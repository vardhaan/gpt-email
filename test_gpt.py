import gpt

gpt = gpt.GPT_Wrapper()


def test_summarization_works():
	example_subject = "SLICE API v2 launch announcement"
	example_body = """SLICE team, 

We’re happy to announce that the SLICE API V2 is now live! Global rollout began this week and we are now at 100%!

Congratulations to the entire team and thank you for all the hard work!

We are monitoring usage and errors with a dashboard and daily war room.

Thanks,
Michelle"""
	response = gpt.summarize_email(example_subject, example_body)
	print(response)
	

test_summarization_works()


