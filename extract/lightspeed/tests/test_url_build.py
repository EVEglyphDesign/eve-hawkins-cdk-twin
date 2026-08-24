"""Smoke tests for URL and $filter construction.

Compares against the verbatim examples in the developer guide:

- Customer/76156733?$top=10&$filter=LastName eq 'simmons' (guide p. 67)
- ServiceDet/76156733?$top=3&$filter=datein ge datetime'2014-01-28T00:00:00' (guide p. 71)
- Deal/76156733?$top=3&$filter=FinanceDate eq datetime'2014-05-16T00:00:00' (guide p. 44)

We build $filter with 'gt' (incremental), not 'eq'/'ge', so the assertions target the
literal formatting and URL segment shape rather than a byte-for-byte match on the guide's
copy-paste examples.

Run: python -m unittest extract.lightspeed.tests.test_url_build
"""
from __future__ import annotations

import unittest

from extract.lightspeed.collect import (
    ApiCfg,
    Endpoint,
    Rooftop,
    build_filter,
    build_url,
)

API = ApiCfg(
    base_url="https://int.lightspeeddataservices.com/lsapi",
    page_size=500,
    gzip_header_name="X-Accept-Encoding",
    connect_timeout_s=15,
    read_timeout_s=120,
    retry_on_status=[500],
    max_retries=3,
    backoff_seconds=[2, 5, 15],
)

ROOFTOP = Rooftop(name="moncton", cmf="76156733", storename="Moncton Peterbilt")


class UrlBuildTests(unittest.TestCase):
    def test_customer_with_storename_and_datetime_watermark(self):
        ep = Endpoint(
            name="Customer",
            incremental_key="DateGathered",
            incremental_type="datetime",
            scope_filter_template="storename eq '{storename}'",
            guide_pages="66-67",
            phase=1,
        )
        url = build_url(API, ep, ROOFTOP, watermark="2026-08-01T00:00:00", skip=0)
        self.assertIn("/lsapi/Customer/76156733?", url)
        self.assertIn("%24top=500", url)
        self.assertIn("%24orderby=DateGathered", url)
        # $filter is one string with both conditions joined by ' and '
        self.assertIn("DateGathered%20gt%20datetime%272026-08-01T00%3A00%3A00%27", url)
        self.assertIn("storename%20eq%20%27Moncton%20Peterbilt%27", url)

    def test_invoicesum_date_watermark_renders_as_datetime_literal(self):
        ep = Endpoint(
            name="InvoiceSum",
            incremental_key="InvoiceDate",
            incremental_type="date",
            scope_filter_template=None,
            guide_pages="96-97",
            phase=1,
        )
        url = build_url(API, ep, ROOFTOP, watermark="2018-07-01", skip=0)
        self.assertIn("/lsapi/InvoiceSum/76156733?", url)
        self.assertIn("InvoiceDate%20gt%20datetime%272018-07-01T00%3A00%3A00%27", url)
        # No $inlinecount, no $select, no $expand
        self.assertNotIn("%24select", url)
        self.assertNotIn("%24inlinecount", url)
        self.assertNotIn("%24expand", url)

    def test_snapshot_endpoint_has_no_filter_or_orderby(self):
        ep = Endpoint(
            name="Customerlasttransaction",
            incremental_key=None,
            incremental_type="none",
            scope_filter_template=None,
            guide_pages="133",
            phase=2,
        )
        url = build_url(API, ep, ROOFTOP, watermark=None, skip=0)
        self.assertIn("/lsapi/Customerlasttransaction/76156733?%24top=500", url)
        self.assertNotIn("%24orderby", url)
        self.assertNotIn("%24filter", url)

    def test_skip_page_two(self):
        ep = Endpoint(
            name="Customer",
            incremental_key="DateGathered",
            incremental_type="datetime",
            scope_filter_template=None,
            guide_pages="66-67",
            phase=1,
        )
        url = build_url(API, ep, ROOFTOP, watermark=None, skip=500)
        self.assertIn("%24top=500", url)
        self.assertIn("%24skip=500", url)

    def test_bigint_watermark_gets_L_suffix(self):
        ep = Endpoint(
            name="ServiceSum",
            incremental_key="ROHeaderId",
            incremental_type="bigint",
            scope_filter_template=None,
            guide_pages="68-69",
            phase=1.5,
        )
        f = build_filter(ep, watermark="735775383867171434", rooftop=ROOFTOP)
        self.assertEqual(f, "ROHeaderId gt 735775383867171434L")


if __name__ == "__main__":
    unittest.main()
