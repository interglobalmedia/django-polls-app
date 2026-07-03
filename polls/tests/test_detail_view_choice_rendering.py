# polls/tests/test_detail_view_choice_rendering.py

import datetime
import re

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Choice, Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text, votes=0):
    """
    Create a choice for the given `question` with the given `choice_text`
    and `votes` count.
    """
    return Choice.objects.create(
        question=question, choice_text=choice_text, votes=votes
    )


def extract_attr(tag_str, attr):
    """Pull a single attribute value out of a raw HTML tag string."""
    match = re.search(rf'{attr}="([^"]*)"', tag_str)
    return match.group(1) if match else None


class DetailViewChoiceRenderingTests(TestCase):
    def test_choice_inputs_and_labels_stay_correctly_paired(self):
        """
        Guards against three known failure patterns in the choice-rendering
        loop:

          1. <input id="..."> and <label for="..."> drifting out of sync
             (e.g. a template edit that changes one but not the other).
          2. The input's id being derived from anything other than the
             loop's own forloop.counter (which silently renders id="").
          3. The input's value being confused with forloop.counter instead
             of the actual choice primary key -- which would send the
             wrong vote to the server on submit.
        """
        past_question = create_question(question_text="Past Question.", days=-5)

        # Create and delete a throwaway choice first, so the primary keys
        # of the choices under test don't coincidentally match their loop
        # position (1, 2, 3). If they matched, a bug that swaps value with
        # forloop.counter could pass by accident.
        throwaway = create_choice(past_question, choice_text="Throwaway.")
        throwaway.delete()

        choice_a = create_choice(past_question, choice_text="Choice A.")
        choice_b = create_choice(past_question, choice_text="Choice B.")
        choice_c = create_choice(past_question, choice_text="Choice C.")
        expected_choices = [choice_a, choice_b, choice_c]

        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        content = response.content.decode()

        input_tags = re.findall(r"<input[^>]*type=\"radio\"[^>]*>", content)
        label_tags = re.findall(r'<label[^>]*for="choice\d+"[^>]*>', content)

        self.assertEqual(
            len(input_tags),
            len(expected_choices),
            "Expected one radio input per choice.",
        )
        self.assertEqual(
            len(label_tags),
            len(expected_choices),
            "Expected one label per choice, in the same order as the inputs.",
        )

        for index, choice in enumerate(expected_choices):
            input_id = extract_attr(input_tags[index], "id")
            input_value = extract_attr(input_tags[index], "value")
            label_for = extract_attr(label_tags[index], "for")

            expected_id = f"choice{index + 1}"

            # 1 & 2: id must follow the forloop.counter pattern -- not
            # blank, not derived from anything else on the choice object.
            self.assertEqual(input_id, expected_id)

            # 1: label's for must match this input's id exactly, so
            # clicking the label activates the correct radio button.
            self.assertEqual(label_for, input_id)

            # 3: the POSTed value must be the choice's real primary key,
            # not the loop counter -- this is what vote() looks up.
            self.assertEqual(input_value, str(choice.id))
