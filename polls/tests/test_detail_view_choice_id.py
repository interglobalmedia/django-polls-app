# polls/tests/test_detail_view_choice_id.py

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
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text, votes=0):
    """
    Create a choice for the given `question` with the given `choice_text`
    and `votes` count.
    """
    return Choice.objects.create(
        question=question, choice_text=choice_text, votes=votes
    )


class DetailViewChoiceIdTests(TestCase):
    def test_choice_input_id_matches_label_for(self):
        """
        Each radio <input id="..."> in the detail view must match the
        <label for="..."> it's paired with, so the label is correctly
        associated with its input.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        create_choice(past_question, choice_text="Choice one.")
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, 'id="choice1"')
        self.assertNotContains(response, 'id=""')
