# Khan Academy Blur Choices

Assessment pages have /e/, /quiz/, or /test/ in their URL.

This fetch-based request always fires when you click the 'Next question' button:
POST https://www.khanacademy.org/api/internal/_analytics/publish_event?type=ContentLibraryNextQuestionButtonClicked&v=2&lang=en&app=khanacademy
