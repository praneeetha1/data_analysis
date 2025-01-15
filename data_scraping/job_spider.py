import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class JobCrawlerSpider(CrawlSpider):
    name = 'job_spider'
    allowed_domains = ["geeksforgeeks.org"]
    start_urls = ["https://www.geeksforgeeks.org/jobs"]
    
    rules = (
        Rule(LinkExtractor(allow='jobs'), callback='parse_job_page', follow=True),
    )
    
    def parse_job_page(self, response):
        job_links = response.css('a::attr(href)').extract()
        
        for link in job_links:
            if 'jobs' in link:
                absolute_url = response.urljoin(link)
                yield scrapy.Request(absolute_url, callback=self.parse_job_details)
    
    def parse_job_details(self, response):
        job_url = response.url
        job_title = response.css('h1::text').get()
        job_description = response.css('.job-description').extract()
        
        # Print out the URL and content
        print(f'Job URL: {job_url}')
        print(f'Job Title: {job_title}')
        print(f'Job Description: {"".join(job_description)}')
        
        yield {
            'job_url': job_url,
            'job_title': job_title,
            'job_description': job_description
        }
