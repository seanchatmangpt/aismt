import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp

from dataclasses import dataclass, field


@dataclass
class SWOTAnalysis:
    """
    Represents a SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis for a company.
    """

    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    threats: list[str] = field(default_factory=list)


@dataclass
class VRIO:
    """
    Represents VRIO (Value, Rarity, Imitability, Organization) factors for a company.

    VRIO analysis is comprehensive, strategically aligned, adaptable, insightful, balanced,
    integrated with other strategic tools, practical, and considerate of stakeholder
    implications. It helps the company identify and leverage its key strengths while
    addressing areas that need improvement to sustain and enhance its competitive position.
    """

    value: str
    rarity: str
    imitability: str
    organization: str


@dataclass
class Financials:
    """
    Represents financial data for a company.
    """

    revenue: int
    profit_margin: float
    major_customers: list[str] = field(default_factory=list)


@dataclass
class MaslowsHierarchyPositioning:
    """
    Represents a company's positioning on Maslow's Hierarchy of Human Needs.

    level: This attribute represents the level of Maslow's Hierarchy that the company primarily addresses.
    The possible values typically are:

    "Physiological": basic needs like food, water, shelter.
    "Safety": personal and financial security, health and wellbeing, safety against accidents/illness.
    "Love/Belonging": friendship, intimacy, family, sense of connection.
    "Esteem": respect, self-esteem, status, recognition, strength, freedom.
    "Self-Actualization": achieving one's full potential, including creative activities.
    relevance: This attribute could describe how the company's products or services meet the needs at the specified level.
     It can also reflect the degree to which the company's offerings are essential or beneficial for satisfying these needs.
    """

    level: str
    relevance: str


@dataclass
class Company:
    """
    Represents information about a company, including SWOT analysis, VRIO factors, Maslow's hierarchy positioning,
    and financials.
    """

    name: str
    swot: SWOTAnalysis
    vrio: VRIO
    maslow_position: MaslowsHierarchyPositioning


@dataclass
class ADSCAnalysis:
    """
    Represents the analysis data for Applied Direct Services Corporation (ADSC) and its competitors.
    """

    competitors: list[Company] = field(default_factory=list)

    def print_swots(self):
        """
        Print SWOT analysis for each company in the analysis.
        """
        for competitor in self.competitors:
            print(f"SWOT Analysis for {competitor.name}:")
            print(f"Strengths: {', '.join(competitor.swot.strengths)}")
            print(f"Weaknesses: {', '.join(competitor.swot.weaknesses)}")
            print(f"Opportunities: {', '.join(competitor.swot.opportunities)}")
            print(f"Threats: {', '.join(competitor.swot.threats)}")
            print("\n")



import streamlit as st
from typing import List

# Import your data structures and analysis classes here

# Define a function to create a Streamlit form
def create_company_form(company: Company):
    st.write(f"## {company.name}")
    st.write("### SWOT Analysis")
    st.write(f"Strengths: {', '.join(company.swot.strengths)}")
    st.write(f"Weaknesses: {', '.join(company.swot.weaknesses)}")
    st.write(f"Opportunities: {', '.join(company.swot.opportunities)}")
    st.write(f"Threats: {', '.join(company.swot.threats)}")

    st.write("### VRIO Factors")
    st.write(f"Value: {company.vrio.value}")
    st.write(f"Rarity: {company.vrio.rarity}")
    st.write(f"Imitability: {company.vrio.imitability}")
    st.write(f"Organization: {company.vrio.organization}")

    st.write("### Maslow's Hierarchy Positioning")
    st.write(f"Level: {company.maslow_position.level}")
    st.write(f"Relevance: {company.maslow_position.relevance}")

# Create a Streamlit app
def main():
    st.title("Company Analysis")

    # Create a sidebar for selecting a company
    selected_company_index = st.sidebar.selectbox(
        "Select a Company",
        [company.name for company in competitors]
    )

    # Find the selected company
    selected_company = None
    for company in competitors:
        if company.name == selected_company_index:
            selected_company = company
            break

    if selected_company:
        create_company_form(selected_company)

# Run the Streamlit app
if __name__ == "__main__":
    competitors=[
        Company(
            name="SCIP",
            swot=SWOTAnalysis(
                strengths=[
                    "expertise in strategic intelligence",
                    "ability to provide customized solutions",
                    "strong network of professionals and experts",
                ],
                weaknesses=[
                    "increasing competition",
                    "need to constantly innovate and adapt",
                    "relatively small team of 88 employees",
                ],
                opportunities=[
                    "expand services to new markets and industries",
                    "develop new products and tools",
                    "leverage strong network and reputation for partnerships",
                ],
                threats=["competition in the market", "changing market conditions"],
            ),
            vrio=VRIO(
                value="Expertise in strategic intelligence and customized solutions",
                rarity="Strong network of professionals and experts",
                imitability="Constant innovation and adaptation",
                organization="Small team of 88 employees",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Esteem",
                relevance="SCIP's key strengths lie in its expertise in strategic intelligence and its ability to provide customized solutions for its clients.",
            ),
        ),
        Company(
            name="Aqute Intelligence",
            swot=SWOTAnalysis(
                strengths=[
                    "Aqute Intelligence is a California-based competitive intelligence company",
                    "Aqute's research techniques are rigorous and exhaustive, making it a reliable source for competitive intelligence",
                    "Aqute's unique community-powered business datasets provide real-time intelligence on an organization's competitors, partners, customers, and prospects",
                ],
                weaknesses=[
                    "Aqute's primary competitors include Cascade Insights, Safos & Thusat, and Aurora WDC",
                    "Aqute has an estimated annual revenue of $100K-5.0M and employs 25-100 people",
                    "Aqute's CEO has a high approval rating among employees",
                ],
                opportunities=[
                    "Aqute offers a variety of tools for gathering competitive intelligence, including tools for analyzing competitors and creating competitor reports",
                    "Aqute also offers import/export information for businesses looking to expand globally",
                ],
                threats=["In 2021, Aqute was acquired by Meltwater for $24.5 million"],
            ),
            vrio=VRIO(
                value="Aqute Intelligence provides valuable competitive intelligence services to businesses.",
                rarity="Aqute Intelligence is one of the few companies that offer community-powered business datasets.",
                imitability="Aqute Intelligence's research techniques are rigorous and exhaustive, making it difficult for competitors to replicate.",
                organization="Aqute Intelligence is strategically aligned, adaptable, and integrated with other strategic tools.",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Esteem",
                relevance="Aqute Intelligence provides services that help businesses gain a competitive edge in their industry, which can be seen as a form of recognition and respect for their clients.",
            ),
        ),
        Company(
            name="ArchIntel™",
            swot=SWOTAnalysis(
                strengths=[
                    "Customized and human-intelligence powered services",
                    "Actionable intelligence and situational awareness",
                    "Dedicated team of researchers",
                    "24/7 information gathering and delivery",
                    "Strong focus on competitors and business trends",
                ],
                weaknesses=[
                    "Reliance on human intelligence may limit scalability",
                    "Limited information on company website",
                    "Limited public information on company's financials and employee count",
                ],
                opportunities=[
                    "Growing demand for competitive intelligence services",
                    "Potential for expansion into new industries and markets",
                    "Partnerships with other companies to enhance services",
                    "Potential for developing new technology to improve information gathering and delivery",
                ],
                threats=[
                    "Intense competition from other competitive intelligence companies",
                    "Potential for data breaches and security threats",
                    "Changes in technology and search engine algorithms may affect information gathering and delivery",
                    "Economic downturns may decrease demand for services",
                ],
            ),
            vrio=VRIO(
                value="Valuable and actionable intelligence for executives and their teams",
                rarity="Customized and human-intelligence powered services",
                imitability="Dedicated team of researchers and tailored search engines",
                organization="Well-organized and efficient system for gathering and delivering information",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Safety",
                relevance="ArchIntel™ helps executives and their teams meet their physiological needs by providing them with valuable information to make informed business decisions and stay ahead of their competitors.",
            ),
        ),
        Company(
            name="SCIP",
            swot=SWOTAnalysis(
                strengths=[
                    "experienced team of professionals",
                    "comprehensive range of services",
                    "strong reputation in the industry",
                ],
                weaknesses=[
                    "limited geographical presence",
                    "reliance on a small number of key clients for a significant portion of its revenue",
                ],
                opportunities=[
                    "expand its services to new markets and industries",
                    "develop new and innovative products",
                    "leverage its strong brand and reputation to attract new clients and partnerships",
                ],
                threats=[
                    "new entrants in the market",
                    "potential disruptions in the industry due to technological advancements",
                    "potential changes in regulations and compliance requirements",
                ],
            ),
            vrio=VRIO(
                value="SCIP's experienced team of professionals, comprehensive range of services, and strong reputation in the industry.",
                rarity="SCIP's strong reputation and track record in the industry is rare and difficult to imitate.",
                imitability="SCIP's expertise and track record in the industry is difficult to imitate.",
                organization="SCIP's strong brand and reputation allows it to attract new clients and partnerships, and its experienced team ensures that its services are strategically aligned, adaptable, insightful, balanced, integrated with other strategic tools, practical, and considerate of stakeholder implications.",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Esteem",
                relevance="SCIP's main focus is on helping businesses gain a competitive advantage through the use of intelligence and research. The company has a strong track record of success and has been able to attract a large number of clients due to its expertise in the field.",
            ),
        ),
        Company(
            name="SIS International Research",
            swot=SWOTAnalysis(
                strengths=[
                    "Established brand and reputation in the market",
                    "Extensive experience and expertise in market research and strategic analysis",
                    "Strong client base, including Fortune 500 companies",
                    "Global presence with offices in New York, Atlanta, London, and Shanghai",
                    "Diverse range of services, including custom market insights, branding, and qualitative fieldwork solutions",
                ],
                weaknesses=[
                    "Limited online presence and digital marketing strategies",
                    "Reliance on traditional market research methods",
                    "High competition in the market research industry",
                    "Limited resources and budget for research and development",
                    "Dependence on a few key clients for a significant portion of revenue",
                ],
                opportunities=[
                    "Growing demand for market research and strategic intelligence services",
                    "Expansion into emerging markets and industries",
                    "Development of new and innovative research methods and technologies",
                    "Strategic partnerships and collaborations with other firms",
                    "Increasing focus on data-driven decision making in businesses",
                ],
                threats=[
                    "Economic downturns and fluctuations in the market research industry",
                    "Rapidly changing technology and market trends",
                    "Intense competition from other market research firms",
                    "Potential loss of key clients to competitors",
                    "Data privacy and security concerns affecting the collection and use of data.",
                ],
            ),
            vrio=VRIO(
                value="Established brand and reputation in the market, Extensive experience and expertise in market research and strategic analysis, Strong client base, including Fortune 500 companies, Diverse range of services, including custom market insights, branding, and qualitative fieldwork solutions",
                rarity="Extensive experience and expertise in market research and strategic analysis, Global presence with offices in New York, Atlanta, London, and Shanghai, Diverse range of services, including custom market insights, branding, and qualitative fieldwork solutions",
                imitability="Established brand and reputation in the market, Extensive experience and expertise in market research and strategic analysis",
                organization="SIS International Research",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Esteem",
                relevance="SIS International Research's primary competitors include Ventana Research, NPD, CNP Global, VDC Research Group, Inc., Simone Smith, and InsideView.",
            ),
        ),
        Company(
            name="One Strategy",
            swot=SWOTAnalysis(
                strengths=[
                    "Large and active community of over 3.5 million business professionals",
                    "Real-time and curated data on competitors, partners, customers, and prospects",
                    "Market research services to help companies stay informed and track industry updates",
                    "Filtering feature for targeted company searches",
                ],
                weaknesses=[
                    "Relatively small annual revenue of $3.3 million",
                    "Limited funding compared to some competitors",
                    "Limited information on company leadership and team",
                ],
                opportunities=[
                    "Potential for growth and expansion with the support of Meltwater",
                    "Opportunity to increase revenue through additional services or partnerships",
                    "Potential to attract more users and increase community size",
                ],
                threats=[
                    "Intense competition from established players such as InsideView and Crunchbase",
                    "Rapidly changing market and industry landscape",
                    "Dependence on user-generated data, which may not always be accurate or up-to-date",
                ],
            ),
            vrio=VRIO(
                value="One Strategy's community-powered business datasets provide valuable and real-time insights on competitors, partners, customers, and prospects",
                rarity="One Strategy's unique community-powered business datasets provide real-time intelligence on an organization's competitors, partners, customers, and prospects",
                imitability="One Strategy's market research services and filtering feature provide a competitive advantage in the market",
                organization="One Strategy's community of over 3.5 million active users and its acquisition by Meltwater demonstrate a strong organizational structure and strategic alignment",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Esteem",
                relevance="One Strategy's community-powered business datasets provide valuable and real-time insights on competitors, partners, customers, and prospects",
            ),
        ),
        Company(
            name="SIS International Research",
            swot=SWOTAnalysis(
                strengths=[
                    "Established brand and reputation in the market",
                    "Extensive experience and expertise in market research and strategic analysis",
                    "Strong client base, including Fortune 500 companies",
                    "Global presence with offices in New York, Atlanta, London, and Shanghai",
                    "Diverse range of services, including custom market insights, branding, and qualitative fieldwork solutions",
                ],
                weaknesses=[
                    "Limited online presence and digital marketing strategies",
                    "Reliance on traditional market research methods",
                    "High competition in the market research industry",
                    "Limited resources and budget for research and development",
                    "Dependence on a few key clients for a significant portion of revenue",
                ],
                opportunities=[
                    "Growing demand for market research and strategic intelligence services",
                    "Expansion into emerging markets and industries",
                    "Development of new and innovative research methods and technologies",
                    "Strategic partnerships and collaborations with other firms",
                    "Increasing focus on data-driven decision making in businesses",
                ],
                threats=[
                    "Economic downturns and fluctuations in the market research industry",
                    "Rapidly changing technology and market trends",
                    "Intense competition from other market research firms",
                    "Potential loss of key clients to competitors",
                    "Data privacy and security concerns affecting the collection and use of data.",
                ],
            ),
            vrio=VRIO(
                value="Established brand and reputation in the market, Extensive experience and expertise in market research and strategic analysis, Strong client base, including Fortune 500 companies, Diverse range of services, including custom market insights, branding, and qualitative fieldwork solutions",
                rarity="Extensive experience and expertise in market research and strategic analysis, Global presence with offices in New York, Atlanta, London, and Shanghai, Diverse range of services, including custom market insights, branding, and qualitative fieldwork solutions",
                imitability="Established brand and reputation in the market, Extensive experience and expertise in market research and strategic analysis",
                organization="SIS International Research",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Esteem",
                relevance="SIS International Research's primary competitors include Ventana Research, NPD, CNP Global, VDC Research Group, Inc., Simone Smith, and InsideView.",
            ),
        ),
        Company(
            name="Cascade Insights",
            swot=SWOTAnalysis(
                strengths=[
                    "Specialized expertise in market research and competitive intelligence for B2B technology companies",
                    "Strong reputation and established client base",
                    "Experienced leadership team with a proven track record",
                    "Comprehensive range of services, including quantitative benchmarking and post-sale customer surveys",
                ],
                weaknesses=[
                    "Relatively small company with 10-100 employees and annual revenues of $1-$10 million",
                    "Limited geographic reach, with a single location in Oregon City, OR",
                    "Dependence on a small number of key clients for a significant portion of revenue",
                ],
                opportunities=[
                    "Growing demand for market research and competitive intelligence services in the B2B technology sector",
                    "Potential for expansion into new geographic markets and industries",
                    "Increasing use of technology and data analytics in market research, providing opportunities for innovation and differentiation",
                ],
                threats=[
                    "Intense competition from larger and more established market research firms",
                    "Economic downturns and budget cuts may lead to reduced demand for market research services",
                    "Rapidly evolving technology landscape may require continuous investment in new tools and techniques to stay competitive",
                ],
            ),
            vrio=VRIO(
                value="Cascade Insights provides valuable insights and intelligence to its clients, helping them make informed business decisions.",
                rarity="The company's specialized expertise in the B2B technology sector is relatively rare, giving it a competitive advantage.",
                imitability="The company's experienced leadership team and comprehensive range of services are difficult to replicate.",
                organization="Cascade Insights has a well-organized and efficient structure, allowing it to deliver high-quality services to its clients.",
            ),
            maslow_position=MaslowsHierarchyPositioning(
                level="Esteem",
                relevance="Cascade Insights helps companies achieve their full potential by providing valuable market insights and intelligence to make informed business decisions.",
            ),
        ),
    ]

    main()