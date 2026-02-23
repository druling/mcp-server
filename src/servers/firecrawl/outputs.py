from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ScrapeResult(BaseModel):
    """Firecrawl scrape result"""
    url: str = Field(description="URL that was scraped")
    title: Optional[str] = Field(default=None, description="Page title")
    content: Optional[str] = Field(default=None, description="Page content")
    markdown: Optional[str] = Field(default=None, description="Content in markdown format")
    html: Optional[str] = Field(default=None, description="Raw HTML content")
    links: Optional[List[str]] = Field(default=None, description="Links found on the page")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class CrawlResult(BaseModel):
    """Firecrawl crawl result"""
    url: str = Field(description="Root URL that was crawled")
    pages: List[ScrapeResult] = Field(description="List of scraped pages")
    count: int = Field(description="Total number of pages crawled")


class Job(BaseModel):
    """Job listing data"""
    title: str = Field(description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    location: Optional[str] = Field(default=None, description="Job location")
    description: Optional[str] = Field(default=None, description="Job description")
    url: Optional[str] = Field(default=None, description="Job posting URL")
    posted_date: Optional[str] = Field(default=None, description="Date posted")


class JobList(BaseModel):
    """List of jobs"""
    jobs: List[Job] = Field(description="List of job postings")
    count: int = Field(description="Total number of jobs")

