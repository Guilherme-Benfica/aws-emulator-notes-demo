def test_save_and_load_note(repo):
    repo.save("n1", "Study for the SAA-C03")
    assert repo.load("n1") == "Study for the SAA-C03"


def test_missing_note_returns_none(repo):
    assert repo.load("does-not-exist") is None


def test_accents_are_preserved(repo):
    repo.save("n2", "Unicode check: São Paulo, café, naïve")
    assert repo.load("n2") == "Unicode check: São Paulo, café, naïve"


def test_overwrite_keeps_latest_text(repo):
    repo.save("n3", "version 1")
    repo.save("n3", "version 2")
    assert repo.load("n3") == "version 2"
