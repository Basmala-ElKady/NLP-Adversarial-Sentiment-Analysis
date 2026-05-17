from app.services.attacker import perform_attack

def test_perform_attack():
    sentence = "This is a great movie"
    result = perform_attack(sentence, "deepwordbug")
    
    assert "perturbed_text" in result
    assert "original_text" in result
    assert result["original_text"] == sentence
    # Note: Sometimes attack might not change text if constraints are too strict, 
    # but for deepwordbug on this sentence it usually does.

def test_attack_invalid_name():
    # Should fallback to default (deepwordbug)
    sentence = "This is a test"
    result = perform_attack(sentence, "invalid_attack_name")
    assert "perturbed_text" in result
    assert result["attack_name"] == "deepwordbug"
