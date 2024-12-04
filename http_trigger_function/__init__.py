""" HTTP trigger function for OpenAI API. """

import logging
import os
import openai
import azure.functions as func
from openai import OpenAIError


def main(req: func.HttpRequest) -> func.HttpResponse:
    """ HTTP trigger function for OpenAI API. """
    logging.info("Python HTTP trigger function processed a request.")

    # Get OpenAI API key from environment variables
    api_key = os.getenv("OPEN_AI_API_KEY")
    if not api_key:
        return func.HttpResponse(
            "OPENAI_API_KEY environment variable is not set.", status_code=500
        )

    # Set the OpenAI API key
    openai.api_key = api_key

    try:
        # Parse the request body
        req_body = req.get_json()
        prompt = req_body.get("prompt", "")

        if not prompt:
            return func.HttpResponse("Prompt is required.", status_code=400)

        # Call OpenAI API
        response = openai.completions.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
        )

        # Return the response
        return func.HttpResponse(
            response.choices[0].text.strip(),
            status_code=200,
            mimetype="application/json",
        )
    except OpenAIError as e:
        logging.error("Error processing request: %s", e)
        return func.HttpResponse(str(e), status_code=500)
