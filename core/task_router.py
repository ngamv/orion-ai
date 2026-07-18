"""Task Router ORION AI"""

ROUTING_RULES = {
    # Développement
    "code":        "backend_dev",
    "bug":         "code_reviewer",
    "api":         "api_dev",
    "database":    "db_dev",
    "mobile":      "mobile_dev",
    "frontend":    "frontend_dev",
    "react":       "frontend_dev",
    "python":      "backend_dev",

    # SEO
    "seo":         "seo_lead",
    "référencement": "seo_lead",
    "google":      "seo_technical",
    "keyword":     "seo_content",

    # Marketing
    "marketing":   "marketing_lead",
    "email":       "email_marketer",
    "pub":         "ads_manager",
    "croissance":  "growth_hacker",
    "marque":      "brand_manager",

    # Social
    "twitter":     "twitter_agent",
    "linkedin":    "linkedin_agent",
    "instagram":   "instagram_agent",
    "tiktok":      "tiktok_agent",
    "social":      "social_lead",

    # DevOps
    "deploy":      "devops_lead",
    "docker":      "cloud_eng",
    "cloud":       "cloud_eng",
    "serveur":     "sre",

    # Sécurité
    "sécurité":    "security_lead",
    "hack":        "pen_tester",
    "vulnérabilité": "pen_tester",

    # QA
    "test":        "qa_lead",
    "bug":         "qa_manual",
    "qualité":     "qa_automation",

    # Design
    "design":      "ui_designer",
    "ux":          "ux_designer",
    "interface":   "ui_designer",

    # Documentation
    "doc":         "doc_lead",
    "guide":       "tech_writer",
    "tutoriel":    "doc_trainer",
}

class TaskRouter:
    def route(self, message: str) -> str:
        message_lower = message.lower()
        for keyword, agent in ROUTING_RULES.items():
            if keyword in message_lower:
                return agent
        return "orion"  # Orion gère par défaut
