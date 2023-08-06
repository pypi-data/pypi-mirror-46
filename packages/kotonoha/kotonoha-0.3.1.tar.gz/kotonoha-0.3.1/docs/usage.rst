=====
Usage
=====

To use Kotonoha in a project::

	from kotonoha import Kotonoha

	jtp = Kotonoha()

	pipeline = [
		{
			'replace_numbers': {'replace_text': '##'}
		},
		{
			'remove_url'
		}
	]

	jtp.prepare(pipeline)
	jtp.run('戦闘力9000以上だ! http://some.url')  # => '戦闘力##以上だ! '


---------------
Getting started
---------------

Kotonoha will execute all tasks defined in the pipeline sequentially.

-------------
List of tasks
-------------

* *alpha_to_full*: Converts all alphabet words to full-width characters (kore => これ).
* *digits*: Converts all numbers to half-width characters (１２３４ => 1234).
* *to_full_width*: Converts to full-width characters (ﾅﾆ => ナニ).
* *lower*: Converts to lower case.
* *replace_numbers*: Replace all numbers with a ```replace_text``` (default #).
* *remove_numbers*: Remove all numbers.
* *replace_prices*: Replace all prices with a ```replace_text``` (default #). Prices should have the format 1,234,567.8912円.
* *remove_prices*: Remove all prices.
* *replace_url*: Replace all urls with a ```replace_text``` (default '').
* *remove_url*: Remove all urls.
* *replace_hashtags*: Replace all hashtags with a ```replace_text``` (default '').
* *replace_emails*: Replace all emails with a ```replace_text``` (default '').
* *replace_mentions*: Replace all mentions with a ```replace_text``` (default '').

-------------
MeCab handler
-------------

There is a class MeCabHandler which can be used to simplify some basic configurations for filtering and lemmatization of words.

	from kotonoha import MeCabHandler
	import MeCab

	tagger = MeCab.Tagger('-Ochasen -d ' + neologd_path)

	handler = MeCabHandler(tagger)

	handler.nouns('...')  # => string containing nouns, separated by spaces, all words are in their lemma format.
	handler.verbs('...')  # => string containing verbs, separated by spaces, all words are in their lemma format.
	handler.meaningful('...')  # => string containing nouns, verbs and adjectives, separated by spaces, all words are in their lemma format.
	handler.basic('...')  # => string containing all words, separated by spaces, all words are in their lemma format.