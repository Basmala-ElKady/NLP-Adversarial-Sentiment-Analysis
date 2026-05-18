from backend.services.attacker import run_attack

def test_run_attack():
    sentence = "This is a great movie"
    result = run_attack(sentence, "deepwordbug")
    
    assert "perturbed_text" in result
    assert "original_text" in result
    assert result["original_text"] == sentence

def test_attack_invalid_name():
    sentence = "This is a test"
    # Should fallback to textattack pipeline and raise ValueError if not found
    try:
        run_attack(sentence, "invalid_attack_name")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
