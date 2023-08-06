from datetime import date
from django.test import TestCase

from botify.bql.exceptions import QueryParsingException
from botify.bql.tests.backends.bigquery import QueryCheckerMixinCollections
from botify.datasources.collections.utils import adapt_crawl_schema_to_collections
from botify.cdf.bql.urls import CrawlSchema
from botify.search_console.bql.crawl import SearchConsoleSchemas


class BaseSearchConsoleWithCrawlSchemaTestCase(TestCase, QueryCheckerMixinCollections):
    def setUp(self):
        self.maxDiff = None
        self.date_start = date(2018, 4, 1)
        self.date_end = date(2018, 5, 20)
        self.revision = {
            "internal": {"gcp_project": "botify-test"},
            "segments": {"names": ["pagetype"]},
        }

    def build_crawl_schema(self, project_id):
        crawl_schema = CrawlSchema(
            crawl_id=2,
            rev_id=3,
            project_id=project_id,
            options={
                "main": {},
                "segments": {"names": ["pagetype"]},
                "content_quality": {},
                "semantic_metadata": {
                    "structured_data": {"versions": {"breadcrumb": 1}},
                    "structured_data_stats": {"breadcrumb": 10},
                },
                "links": {"top_anchors": True},
            },
            with_fk_fields=True,
        )
        crawl_schema.update_prefix("crawl")
        adapt_crawl_schema_to_collections(crawl_schema)
        return crawl_schema

    def build_search_console_schemas(self, project_id):
        return SearchConsoleSchemas(
            project_id,
            self.date_start,
            self.date_end,
            self.revision,
            with_urls_and_segments=True,
        )

    def get_schemas(self):
        project_id = 1
        crawl_schema = self.build_crawl_schema(project_id)
        schemas = self.build_search_console_schemas(project_id)
        schemas.schemas = [crawl_schema] + schemas.schemas
        return schemas


class SearchConsoleFilterMultipleTableTestCase(
    BaseSearchConsoleWithCrawlSchemaTestCase
):
    def test_filter_on_dimensions(self):
        bql = {
            "dimensions": [
                "segments.pagetype.value",
                "date",
                {
                    "field": "crawl.http_code",
                    "ranges": [{"from": 300}, {"from": 200, "to": 300}, {"to": 200}],
                },
            ],
            "metrics": ["search_console.count_impressions", {"avg": "crawl.depth"}],
            "filters": {
                "and": [
                    {
                        "field": "search_console.keyword",
                        "predicate": "contains",
                        "value": "happiness",
                    },
                    {"field": "crawl.byte_size", "predicate": "gt", "value": 30},
                    {
                        "field": "search_console.count_urls",
                        "predicate": "gt",
                        "value": 500,
                    },
                ]
            },
        }
        expected = """
SELECT COALESCE(sq_1.segments__pagetype__value, sq_2.segments__pagetype__value) f_0,
sq_2.date f_1,
CASE WHEN sq_1.http_code >= 300 THEN '0000_from_300_to_'
WHEN sq_1.http_code >= 200 AND sq_1.http_code < 300 THEN '0001_from_200_to_300'
WHEN sq_1.http_code < 200 THEN '0002_from__to_200'
END f_2,
IFNULL(SUM(sq_2.impressions), 0) f_3,
avg(sq_1.depth) f_4

FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(segments__pagetype__value) segments__pagetype__value,
ANY_VALUE(url_hash) url_hash,
date,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY date, url_keyword_hash) sq_2

ON sq_1.url_hash = sq_2.url_hash

WHERE (sq_2.keyword LIKE '%happiness%' AND sq_1.byte_size > 30) AND sq_2.date IS NOT NULL
GROUP BY f_0, f_1, f_2
HAVING APPROX_COUNT_DISTINCT(sq_2.url_hash) > 500
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_on_global_dimensions(self):
        bql = {
            "dimensions": ["url"],
            "metrics": ["search_console.count_impressions", {"avg": "crawl.http_code"}],
            "filters": {"field": "protocol", "predicate": "contains", "value": "http"},
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
IFNULL(SUM(sq_2.impressions), 0) f_1,
avg(sq_1.http_code) f_2

FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(protocol) protocol,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) sq_2

ON sq_1.url_hash = sq_2.url_hash

WHERE COALESCE(sq_1.protocol, sq_2.protocol) LIKE '%http%'
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_subquery(self):
        bql = {
            "dimensions": ["url"],
            "metrics": ["search_console.ctr", {"avg": "crawl.http_code"}],
            "filters": {
                "and": [
                    {
                        "field": "url",
                        "predicate": "query",
                        "value": {
                            "filters": {
                                "field": "search_console.avg_position",
                                "predicate": "lte",
                                "value": 11,
                            }
                        },
                    },
                    {
                        "field": "search_console.avg_position",
                        "predicate": "lte",
                        "value": 12,
                    },
                ]
            },
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
((SUM(sq_2.clicks) / SUM(sq_2.impressions)) * 100) f_1,
avg(sq_1.http_code) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT (SUM((impressions * avg_position)) / SUM(impressions)) avg_position,
(SUM((impressions * avg_position)) / SUM(impressions)) search_console__avg_position,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE sq_2.search_console__avg_position <= 11
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
HAVING (SUM((sq_2.impressions * sq_2.avg_position)) / SUM(sq_2.impressions)) <= 12
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_subquery_with_query_field(self):
        bql = {
            "dimensions": ["url"],
            "metrics": ["search_console.count_impressions", {"avg": "crawl.http_code"}],
            "filters": {
                "field": "url",
                "predicate": "query",
                "value": {
                    "filters": {
                        "field": "search_console.count_impressions",
                        "predicate": "gt",
                        "value": 100,
                    }
                },
            },
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
IFNULL(SUM(sq_2.impressions), 0) f_1,
avg(sq_1.http_code) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
SUM(impressions) search_console__count_impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE sq_2.search_console__count_impressions > 100
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_subquery_with_global_field(self):
        bql = {
            "dimensions": ["url"],
            "metrics": ["search_console.count_impressions", {"avg": "crawl.http_code"}],
            "filters": {"field": "segments.pagetype.depth_1", "value": "foo"},
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
IFNULL(SUM(sq_2.impressions), 0) f_1,
avg(sq_1.http_code) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(segments__pagetype__depth_1) segments__pagetype__depth_1,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword),
segments__pagetype__depths[SAFE_OFFSET(0)] segments__pagetype__depth_1
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE COALESCE(sq_1.segments__pagetype__depth_1, sq_2.segments__pagetype__depth_1) = 'foo'
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_global_field_not_on_crawl(self):
        bql = {
            "dimensions": ["url"],
            "metrics": [
                "search_console.count_impressions",
                {
                    "function": "add",
                    "args": [
                        "search_console.count_impressions",
                        {"avg": "crawl.http_code"},
                    ],
                },
            ],
            "filters": {"field": "keyword_meta.branded", "value": True},
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
IFNULL(SUM(sq_2.impressions), 0) f_1,
(IFNULL(SUM(sq_2.impressions), 0) + avg(sq_1.http_code)) f_2

FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(branded) branded,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) sq_2

ON sq_1.url_hash = sq_2.url_hash
WHERE sq_2.branded
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_subquery_filter_metric_with_dimension_one_schema(self):
        bql = {
            "dimensions": ["date"],
            "metrics": ["search_console.count_impressions", {"avg": "crawl.http_code"}],
            "filters": {
                "and": [
                    {"field": "keyword_meta.branded", "value": True},
                    {"field": "crawl.byte_size", "predicate": "gt", "value": 4},
                ]
            },
        }
        expected = """
SELECT sq_2.date f_0,
IFNULL(SUM(sq_2.impressions), 0) f_1,
avg(sq_1.http_code) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(branded) branded,
ANY_VALUE(url_hash) url_hash,
date,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY date, url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE (sq_2.branded AND sq_1.byte_size > 4) AND sq_2.date IS NOT NULL
GROUP BY f_0
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_for_url_explorer(self):
        bql = {
            "dimensions": ["url", "keyword", "crawl.http_code"],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
sq_1.http_code f_2,
IFNULL(SUM(sq_2.impressions), 0) f_3
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), f_2, sq_2.keyword_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_search_console_dimension_not_on_crawl(self):
        bql = {
            "dimensions": ["segments.pagetype.depth_1"],
            "metrics": [
                {"avg": "crawl.depth"},
                {"function": "sub", "args": [100, {"avg": "crawl.depth"}]},
            ],
            "filters": {
                "field": "keyword_meta.branded",
                "predicate": "eq",
                "value": False,
            },
        }
        expected = """
SELECT COALESCE(sq_1.segments__pagetype__depth_1, sq_2.segments__pagetype__depth_1) f_0,
avg(sq_1.depth) f_1,
(100 - avg(sq_1.depth)) f_2

FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(branded) branded,
ANY_VALUE(segments__pagetype__depth_1) segments__pagetype__depth_1,
ANY_VALUE(url_hash) url_hash,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword),
segments__pagetype__depths[SAFE_OFFSET(0)] segments__pagetype__depth_1
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY url_keyword_hash) sq_2

ON sq_1.url_hash = sq_2.url_hash

WHERE NOT(sq_2.branded)
GROUP BY f_0
"""  # NOQA  sqlformat
        self.check_query(expected, bql)


class SpecificFieldSearchConsoleAndCrawlTestCase(
    BaseSearchConsoleWithCrawlSchemaTestCase
):
    def test_keyword_position_for_url(self):
        bql = {
            "dimensions": ["url", "keyword"],
            "metrics": [
                "search_console.keyword_position_for_url",
                {"avg": "crawl.depth"},
            ],
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
ANY_VALUE(sq_2.keyword_position_for_url) f_2,
avg(sq_1.depth) f_3
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
ROW_NUMBER() OVER (PARTITION BY ANY_VALUE(url_hash) ORDER BY SUM(clicks) DESC) keyword_position_for_url,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), sq_2.keyword_hash
        """
        self.check_query(expected, bql)

    def test_full_breadcrumb_name_dimension(self):
        bql = {
            "dimensions": [
                "url",
                "keyword",
                "crawl.metadata.structured.breadcrumb.full_breadcrumb_name",
            ],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
IF(ARRAY_LENGTH(metadata__structured__breadcrumb__names) = 0, NULL, ARRAY_TO_STRING(metadata__structured__breadcrumb__names, ' > ')) f_2,
IFNULL(SUM(sq_2.impressions), 0) f_3
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), f_2, sq_2.keyword_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_full_breadcrumb_name_filter(self):
        bql = {
            "dimensions": ["url", "keyword"],
            "metrics": ["search_console.count_impressions"],
            "filters": {
                "field": "crawl.metadata.structured.breadcrumb.full_breadcrumb_name",
                "predicate": "contains",
                "value": "Sales",
            },
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
IFNULL(SUM(sq_2.impressions), 0) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE IF(ARRAY_LENGTH(metadata__structured__breadcrumb__names) = 0, NULL, ARRAY_TO_STRING(metadata__structured__breadcrumb__names, ' > ')) LIKE '%Sales%'
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), sq_2.keyword_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_http_redirect_was_crawled(self):
        bql = {
            "metrics": [
                {"field": "search_console.count_rankings"},
                {"field": "search_console.count_clicks"},
            ],
            "dimensions": [{"field": "search_console.country"}],
            "filters": {
                "and": [
                    {
                        "field": "search_console.keyword_meta.branded",
                        "predicate": "eq",
                        "value": False,
                    },
                    {
                        "predicate": "eq",
                        "value": True,
                        "field": "crawl.http_redirect.to.crawled",
                    },
                ]
            },
        }
        expected = """
SELECT sq_1.country f_0,
APPROX_COUNT_DISTINCT(sq_1.url_keyword_hash) f_1,
IFNULL(SUM(sq_1.clicks), 0) f_2
FROM (SELECT ANY_VALUE(branded) branded,
ANY_VALUE(url_hash) url_hash,
country,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
JOIN
(SELECT * EXCEPT (url_hash, keyword_hash, url, keyword)
FROM (SELECT *,
ROW_NUMBER() OVER (PARTITION BY url_keyword_hash) AS rn
FROM `botify-test.test_1.search_console_unique_url_kw_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180501")
WHERE rn = 1)
USING (url_keyword_hash)
GROUP BY country, url_keyword_hash) sq_1
FULL OUTER JOIN
(SELECT *
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) a
LEFT JOIN
(SELECT http_code http_redirect__to__http_code,
url_id,
url_id http_redirect__to__url_id
FROM test_1.crawl_2_3) b
ON a.redirect__to__url.url_id = b.url_id) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE (NOT(sq_1.branded) AND (sq_2.http_redirect__to__url_id IS NOT NULL AND sq_2.http_redirect__to__http_code > 0)) AND sq_1.country IS NOT NULL
GROUP BY f_0
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_http_redirect_is_compliant(self):
        bql = {
            "metrics": ["search_console.count_clicks"],
            "dimensions": ["url"],
            "filters": {
                "predicate": "eq",
                "value": True,
                "field": "crawl.http_redirect.to.compliant.is_compliant",
            },
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
IFNULL(SUM(sq_2.clicks), 0) f_1
FROM (SELECT *
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) a
LEFT JOIN
(SELECT compliant__is_compliant crawl__http_redirect__to__compliant__is_compliant,
url_id
FROM test_1.crawl_2_3) b
ON a.redirect__to__url.url_id = b.url_id) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE sq_1.crawl__http_redirect__to__compliant__is_compliant
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
"""  # NOQA  sqlformat
        self.check_query(expected, bql)


class SearchConsoleCrawlMultipleFieldsTestCase(
    BaseSearchConsoleWithCrawlSchemaTestCase
):
    def test_multiple_field_forbidden_alone(self):
        bql = {
            "dimensions": ["crawl.metadata.structured.breadcrumb.names"],
            "metrics": ["search_console.count_impressions"],
        }
        with self.assertRaises(QueryParsingException):
            self.transform_query(bql)

    def test_multiple_field_forbidden_with_irrelevant_field(self):
        bql = {
            "dimensions": ["keyword", "crawl.content_quality.samples"],
            "metrics": ["search_console.count_impressions"],
        }
        with self.assertRaises(QueryParsingException):
            self.transform_query(bql)

    def test_multiple_field_allowed_with_pk(self):
        bql = {
            "dimensions": ["url", "crawl.content_quality.samples"],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_1.content_quality__samples) f_1,
IFNULL(SUM(sq_2.impressions), 0) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2

ON sq_1.url_hash = sq_2.url_hash
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_multiple_field_one_schema(self):
        bql = {
            "dimensions": ["url", "crawl.content_quality.samples"],
            "metrics": [{"avg": "crawl.depth"}],
        }
        expected = """
SELECT ANY_VALUE(sq_1.url) f_0,
ANY_VALUE(sq_1.content_quality__samples) f_1,
avg(sq_1.depth) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
GROUP BY sq_1.url_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_multiple_field_allowed_with_pk_and_other_field(self):
        bql = {
            "dimensions": ["url", "keyword", "crawl.content_quality.samples"],
            "metrics": ["search_console.count_impressions"],
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
ANY_VALUE(sq_1.content_quality__samples) f_2,
IFNULL(SUM(sq_2.impressions), 0) f_3
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), sq_2.keyword_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_multiple_field_multiple_schemas(self):
        bql = {
            "dimensions": ["url", "crawl.content_quality.samples"],
            "metrics": ["search_console.count_impressions", {"avg": "crawl.depth"}],
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_1.content_quality__samples) f_1,
IFNULL(SUM(sq_2.impressions), 0) f_2,
avg(sq_1.depth) f_3
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash)
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_index_field(self):
        bql = {
            "dimensions": [
                "url",
                "keyword",
                "crawl.metadata.h1.contents[0]",
                "crawl.metadata.h1.contents[1]",
            ],
            "metrics": ["search_console.count_clicks"],
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
sq_1.metadata__h1__contents[SAFE_OFFSET(0)] f_2,
sq_1.metadata__h1__contents[SAFE_OFFSET(1)] f_3,
IFNULL(SUM(sq_2.clicks), 0) f_4
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1
FULL OUTER JOIN
(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), f_2, f_3, sq_2.keyword_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_multiple_field(self):
        bql = {
            "dimensions": ["url", "keyword", "crawl.metadata.h1.contents"],
            "metrics": ["search_console.count_clicks"],
            "filters": {
                "field": "crawl.metadata.h1.contents",
                "predicate": "any.contains",
                "value": "I need beer",
            },
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
ANY_VALUE(sq_1.metadata__h1__contents) f_2,
IFNULL(SUM(sq_2.clicks), 0) f_3
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(clicks) clicks,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash
WHERE EXISTS(SELECT 1
FROM UNNEST(sq_1.metadata__h1__contents) AS a
WHERE a LIKE '%I need beer%')
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), sq_2.keyword_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)

    def test_filter_multiple_fields(self):
        bql = {
            "dimensions": ["url", "keyword"],
            "metrics": ["search_console.count_impressions"],
            "filters": {
                "or": [
                    {
                        "field": "crawl.inlinks_internal.anchors.top.text",
                        "predicate": "any.contains",
                        "value": "lorem",
                    },
                    {
                        "field": "crawl.inlinks_internal.anchors.top.text",
                        "predicate": "all.eq",
                        "value": "foobar",
                    },
                ]
            },
        }
        expected = """
SELECT ANY_VALUE(COALESCE(sq_1.url, sq_2.url)) f_0,
ANY_VALUE(sq_2.keyword) f_1,
IFNULL(SUM(sq_2.impressions), 0) f_2
FROM (SELECT *
FROM test_1.crawl_2_3
WHERE http_code <> 0) sq_1

FULL OUTER JOIN

(SELECT ANY_VALUE(keyword) keyword,
ANY_VALUE(keyword_hash) keyword_hash,
ANY_VALUE(url) url,
ANY_VALUE(url_hash) url_hash,
SUM(impressions) impressions,
url_keyword_hash
FROM (SELECT *
FROM `botify-test.test_1.search_console_2*`
WHERE _TABLE_SUFFIX BETWEEN "0180401" AND "0180520")
GROUP BY url_keyword_hash) sq_2
ON sq_1.url_hash = sq_2.url_hash

WHERE (EXISTS(SELECT 1
FROM UNNEST(sq_1.inlinks_internal__anchors__top__text) AS a
WHERE a LIKE '%lorem%') OR (SELECT SUM(1)
FROM UNNEST(sq_1.inlinks_internal__anchors__top__text) AS a
WHERE a = 'foobar') = ARRAY_LENGTH(sq_1.inlinks_internal__anchors__top__text))
GROUP BY COALESCE(sq_1.url_hash, sq_2.url_hash), sq_2.keyword_hash
"""  # NOQA  sqlformat
        self.check_query(expected, bql)
