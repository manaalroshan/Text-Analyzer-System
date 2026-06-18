from text_analyzer import TextCleaner, EntityAnalyzer, AnalysisContext
from config import email_pattern, url_pattern, phone_pattern, date_pattern

def test_entity_analyzer_whole_pipeline():
    context = AnalysisContext("dummy")
    context.raw_text = "Contact John at john.doe@example.com or jane.smith@company.org. Call +1-555-123-4567 or (212) 555-7890 for assistance. The meeting is scheduled for 15/06/2026, and the follow-up is on June 20, 2026. Visit https://www.example.com or https://support.company.org/help for details. For urgent issues, email support@service.net or admin@test.co.in. Reach us at +91 98765 43210 or 080-1234-5678. Registration closes on 2026-07-01, and results will be announced on 07/15/2026. More information is available at http://testsite.org and https://docs.example.com/api."
    context.email = TextCleaner.email_extractor(context.raw_text, email_pattern)
    context.url = TextCleaner.url_extractor(context.raw_text, url_pattern, email_pattern)
    context.phone = TextCleaner.phone_extractor(context.raw_text, phone_pattern)
    context.date = TextCleaner.date_extractor(context.raw_text, date_pattern)
    analyzer = EntityAnalyzer()
    result = analyzer.analyze(context)
    assert result['Emails'] == ["john.doe@example.com", "jane.smith@company.org", "support@service.net", "admin@test.co.in"]
    assert result['Urls'] == ["https://www.example.com", "https://support.company.org/help", "http://testsite.org", "https://docs.example.com/api"]
    assert result['Phone Numbers'] == ["+1-555-123-4567", "(212) 555-7890", "+91 98765 43210", "080-1234-5678"]
    assert result['Dates'] == ["15/06/2026", "June 20, 2026", "2026-07-01", "07/15/2026"]