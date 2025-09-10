# resto-finder

Search a restaurant through natural language.

## Running locally

1. Clone this repo.

2. Rename the `.env.sample` file to `.env` and provide the `FOURSQUARE_API_KEY`, `LLM_SERVER_URL`, `LLM_API_KEY`.

3. Quickest way to run is by Docker. An `instructions.txt` is provided that has 2 copy-pastable commands to start the app.

## Limitations

### FOURSQUARE Places API

Restaurant details such as the Cuisine, Rating, Price Level, Operating Hours are only available for users who have Premium subscription. Therefore, these details are not returned when using the resto-finder app.

References: [Places Response Fields](https://docs.foursquare.com/fsq-developers-places/reference/response-fields), [Pricing](https://foursquare.com/pricing/#places_api)

### Gemini API

The app will throw an error if using Gemini models. The error specifically is due to constraining the output to JSON by using a schema, which the Gemini API handle differently. There's work going on for [Gemini API to OpenAI library compatibility](https://ai.google.dev/gemini-api/docs/openai) but this particular feature is still not supported.