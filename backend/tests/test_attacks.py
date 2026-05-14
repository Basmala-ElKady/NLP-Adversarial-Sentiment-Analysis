from app.services.attacks import (
    leetspeak_attack
)


def test_leetspeak_attack():

    sentence = "This is amazing"

    attacked = leetspeak_attack(
        sentence
    )

    assert attacked != sentence
