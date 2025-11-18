# Lyrics Tools - Enhancements To Be Determined
This document outlines potential enhancements for the Lyrics Tools application. These features are proposed to improve user experience, expand functionality, and increase the versatility of the tool. Feedback and suggestions from users are welcome to help prioritize and refine these enhancements.

## Planned Enhancements

## MVP 1.1.1
    TODO: Eliminate the need to re-enter the OpenAI API key on each run.
        Enter OPENAI_API_KEY only ONCE in the sidebar when the app opens for the first time.  
        Then store the key in a local `.env` file for future runs.
        Make sure to add `.env` to your `.gitignore` to avoid committing sensitive info.
        Then hide the sidebar with the top-left hamburger menu.

MVP 1.1.2
- **Enhanced error handling**: Provide more detailed feedback for common issues like invalid API keys or network errors.
- **Export Lyrics options**: Download song meanings as text or CSV files for offline use.
- **Export Explanation options**: Download song meanings as text or CSV files for offline use.
- **Customizable prompts**: Allow users to modify the prompt template for more tailored outputs.

MVP 1.1.3
- **Automatically extract lyrics**: from a provided URL (e.g., Genius, AZLyrics).
- **Multi-language support**: Analyze song meanings in languages other than English.

## MVP 1.2.0 ??
- **Batch processing**: Upload a CSV of songs to get meanings for multiple entries at once.


## MVP 1.5.0+
- **User accounts**: Save preferences and history with user authentication for lyrics websites.

## MVP 1.2.0 
- **Integration with music APIs**: Fetch lyrics directly from services like Spotify or Genius.
- **Mobile-friendly UI**: Optimize the interface for use on smartphones and tablets.
- **Performance optimizations**: Speed up response times with caching or more efficient API usage.
- **Collaboration features**: Share song analyses with others via links or social media.
- **Thematic tagging**: Automatically tag songs with themes or genres based on their meanings.
- **Voice input**: Allow users to speak song titles or lyrics for analysis.
- **Dark mode toggle**: Let users switch between light and dark themes for better accessibility.
- **Feedback loop**: Enable users to rate the quality of the song meanings to improve future outputs.

## MVP 2.0+
- **Advanced analytics**: Visualize trends in song themes and meanings across different genres or time periods.
