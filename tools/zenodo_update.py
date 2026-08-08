#!/usr/bin/env python3
"""Update the trilogy's Zenodo records to v1.0.

Run OUTSIDE the sandboxed session, on a machine with normal network access.

    export ZENODO_TOKEN=...              # personal access token (deposit:write + deposit:actions)
    python tools/zenodo_update.py fetch              # step 1: print concept DOIs, change nothing
    python tools/zenodo_update.py publish <pdf_dir>  # step 3: new version, upload, publish

`fetch` prints each record's concept DOI ("cite all versions") so the papers'
companion bibitems can be switched to them BEFORE the new PDFs are built and
uploaded. `publish` then, for each record: creates a new version draft, removes
the old file, uploads the new PDF from <pdf_dir>, sets version/date metadata,
and publishes. The token is read from the environment only; never write it to
a file or commit it.

Requires: pip install requests
"""
import os
import sys

import requests

API = "https://zenodo.org/api"

# record id -> (pdf filename, one-line change note for the description)
RECORDS = {
    "21769103": ("prime_sum_formula_paper.pdf",
                 "v1.0: literature-review revision (expanded bibliography and related-work "
                 "positioning, keywords and MSC 2020 added); mathematical content unchanged."),
    "21769105": ("prime_ladder_paper.pdf",
                 "v1.0: literature-review revision (expanded bibliography, bibliographic "
                 "corrections, keywords and MSC 2020 added); mathematical content unchanged."),
    "21769107": ("prime_recovery_paper.pdf",
                 "v1.0: literature-review revision (expanded bibliography and related-work "
                 "positioning, keywords and MSC 2020 added); mathematical content unchanged."),
}

VERSION = "1.0"
PUB_DATE = "2026-08-08"


def token():
    t = os.environ.get("ZENODO_TOKEN")
    if not t:
        sys.exit("Set ZENODO_TOKEN in the environment first.")
    return t


def fetch():
    for recid in RECORDS:
        r = requests.get(f"{API}/records/{recid}", timeout=30)
        r.raise_for_status()
        j = r.json()
        print(f"record {recid}: title = {j['metadata']['title']!r}")
        print(f"  version DOI : {j.get('doi', '?')}")
        print(f"  concept DOI : {j.get('conceptdoi', '?  (not shown -- check the record page)')}")


def publish(pdf_dir):
    params = {"access_token": token()}
    for recid, (pdf_name, note) in RECORDS.items():
        pdf_path = os.path.join(pdf_dir, pdf_name)
        if not os.path.isfile(pdf_path):
            sys.exit(f"missing PDF: {pdf_path}")

        print(f"== record {recid}: creating new version ...")
        r = requests.post(f"{API}/deposit/depositions/{recid}/actions/newversion",
                          params=params, timeout=60)
        r.raise_for_status()
        draft_url = r.json()["links"]["latest_draft"]

        r = requests.get(draft_url, params=params, timeout=30)
        r.raise_for_status()
        draft = r.json()
        draft_id = draft["id"]

        for f in draft.get("files", []):
            requests.delete(f"{API}/deposit/depositions/{draft_id}/files/{f['id']}",
                            params=params, timeout=60).raise_for_status()
            print(f"   removed old file {f['filename']}")

        bucket = draft["links"]["bucket"]
        with open(pdf_path, "rb") as fh:
            r = requests.put(f"{bucket}/{pdf_name}", data=fh, params=params, timeout=300)
            r.raise_for_status()
        print(f"   uploaded {pdf_name}")

        md = draft["metadata"]
        md["version"] = VERSION
        md["publication_date"] = PUB_DATE
        if note not in md.get("description", ""):
            md["description"] = md.get("description", "").rstrip() + f"\n<p>{note}</p>"
        r = requests.put(f"{API}/deposit/depositions/{draft_id}",
                         json={"metadata": md}, params=params, timeout=60)
        r.raise_for_status()

        r = requests.post(f"{API}/deposit/depositions/{draft_id}/actions/publish",
                          params=params, timeout=120)
        r.raise_for_status()
        j = r.json()
        print(f"   PUBLISHED: new version DOI = {j.get('doi')}")
        print(f"              concept DOI     = {j.get('conceptdoi')}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "fetch":
        fetch()
    elif len(sys.argv) >= 3 and sys.argv[1] == "publish":
        publish(sys.argv[2])
    else:
        sys.exit(__doc__)
