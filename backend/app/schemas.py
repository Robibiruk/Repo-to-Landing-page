from pydantic import BaseModel, Field


class FeatureCard(BaseModel):
    title: str
    blurb: str
    iconKey: str = Field(default="spark")


class Brand(BaseModel):
    name: str
    tagline: str
    accent: str = Field(default="#6366f1", description="Hex color, e.g. #6366f1")
    gradientFrom: str = Field(default="#6366f1")
    gradientTo: str = Field(default="#22d3ee")


class Hero(BaseModel):
    headline: str
    subheadline: str
    cta: str


class InstallSection(BaseModel):
    heading: str = "Get started"
    commands: list[str] = []
    snippet: str = ""


class FooterLink(BaseModel):
    label: str
    url: str


class Footer(BaseModel):
    license: str = ""
    links: list[FooterLink] = []


class Seo(BaseModel):
    title: str
    description: str
    keywords: list[str] = []


class LandingContent(BaseModel):
    brand: Brand
    hero: Hero
    problem: str
    solution: str
    features: list[FeatureCard] = Field(default_factory=list)
    install: InstallSection = InstallSection()
    sections: list[str] = Field(default_factory=list, description="Extra section types: examples, roadmap, pricing, faq, stats, team")
    footer: Footer = Footer()
    seo: Seo
