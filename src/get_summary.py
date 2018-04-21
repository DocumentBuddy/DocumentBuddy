# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "german"
SENTENCES_COUNT = 5
text = """
Unternehmensfinanzierung im Umbruch

Die Finanzierungsperspektiven deutscher Unternehmen im Zeichen
von Finanzmarktwandel und Basel II

Auswertung der Unternehmensbefragung 2001
(Kurzfassung)



Neue Informations- und Kommunikationstechnologien, Deregulierung und Reregulie-
rung sowie die Globalisierung der Märkte einerseits und ein stärker risiko- und er-
tragsbewusstes Verhalten von Anlegern und Aktionären andererseits führen sowohl
zu mehr Wettbewerb auf den Finanzmärkten als auch zu einem stärker risikobe-
wussten Verhalten der Kreditinstitute.
Mit dem Ziel herauszufinden, ob die Unternehmen den Wandel auf den Finanzmärk-
ten bereits heute spüren und wie sie die Zukunft der Unternehmensfinanzierung se-
hen, haben KfW und 20 Wirtschaftsverbände gemeinsam im September und Oktober
2001 eine umfassende Befragung durchgeführt. Mit weit über 6000 Antworten von
Unternehmen aller Branchen, Größenklassen und Rechtsformen wird ein zutreffen-
des Bild der Realität gezeichnet.
Die Hauptergebnisse lassen sich wie folgt zusammenfassen:
1. Zum ersten Mal gibt es konkrete empirische Belege dafür, dass sich die Kredit-

vergabepolitik der Banken geändert hat: Sie wird differenzierter und in der Ten-
denz restriktiver. Das hängt damit zusammen, dass die Banken eine intensivere
Rating-gestützte Kreditprüfung durchführen, die Konditionen zwischen guten und
weniger guten Bonitäten stärker differenzieren und versuchen, die niedrigen Mar-
gen im Firmenkundenkredit zu erhöhen.

2. Der Wandel ist in vollem Gange: Die Finanzierungsbedingungen sind bereits für
ein knappes Drittel aller Unternehmen schwieriger geworden. Gleichzeitig gibt es
für eine kleine Minderheit auch bessere Finanzierungsbedingungen, zwei Drittel
spüren noch keine Auswirkungen.

3. Die Schwierigkeiten machen sich besonders bei kleinen Unternehmen, aber auch
bei den großen Unternehmen bemerkbar. Die mittelgroßen Unternehmen spüren
den Wandel weniger stark; aber auch sie werden sich der Entwicklung nicht ent-
ziehen können. Konjunkturell angeschlagene Branchen (Einzelhandel, Bau) und
Unternehmen in Ostdeutschland sind vom Wandel besonders stark betroffen.

4. Besonders deutlich zeigen sich die Schwierigkeiten bei der Investitionsfinanzie-
rung und hier zeigt sich ein eindeutiger Größentrend - d. h. je kleiner die Unter-
nehmen, desto eher verschlechtern sich die Finanzierungsbedingungen.

5. Viele Unternehmen, die sich für Förderkredite qualifizieren, nutzen dieses Ange-
bot noch nicht. Viele Banken informieren ihre Kunden über Förderangebote. Die-
ser Service ist in Ostdeutschland schwächer ausgeprägt als in Westdeutschland
und vor allem gegenüber kleineren Unternehmen noch ausbaufähig. Hier liegt
offensichtlich ein Informationsdefizit vor, an dem alle – Unternehmen, Verbände,
Kreditinstitute und Förderbanken – weiter arbeiten müssen.

6. Das Spektrum der Finanzierungsinstrumente, die auch kleinen und mittleren Un-
ternehmen zugänglich sind, wird breiter. Alle Unternehmen messen Finanzie-
rungsfragen heutzutage eine stärkere Bedeutung zu als früher, und sie werden
intensiver als bisher Finanzierungsalternativen auf Kosten und Erträge prüfen.

7. Die vorherrschende Fremdfinanzierungskultur in Deutschland wird sich vorerst
zwar nicht grundlegend ändern. Aber viele Unternehmen – auch kleinere – pla-
nen, in Zukunft neben den traditionellen auch bisher ungenutzte Finanzierungsin-
strumente einzusetzen und neue Finanzierungsquellen zu erschließen. Insbeson-
dere die Finanzierung durch Beteiligungskapital wird an Bedeutung gewinnen.



2

8. Die Mehrzahl der Unternehmen befürchtet von Basel II negative Auswirkungen,
und zwar häufiger, wenn sie schlechter informiert sind. Ihr Informationsstand
steigt - wenn er auch noch nicht ausreichend ist, vor allem bei kleineren und ost-
deutschen Unternehmen. Hier herrscht noch Informationsbedarf, und Politik, Ver-
bände und Kreditinstitute sind gefordert.

9. Viele Unternehmen wollen versuchen, ihre Bonitätseinstufung im Hinblick auf Ba-
sel II zu verbessern. Einige setzen auf mehr Transparenz und Kommunikation mit
ihrer Bank, andere ziehen ein externes Rating in Erwägung. Nicht wenige ver-
sprechen sich eine Bonitätsverbesserung von einer Erhöhung ihrer Eigenmittel-
quote.

Die KfW kann den erforderlichen Wandel bei der Unternehmensfinanzierung durch
die Weiterentwicklung der Mittelstandsförderung wirkungsvoll unterstützen. Sie ist
dabei, ihre Geschäftspolitik in diesem Sinne neu auszurichten und hat die wichtigsten
Schritte auf dem Weg zu einem neuen Förderinstrumentarium bereits getan.
Das Angebot von und die Nachfrage nach alternativen Finanzierungsformen und -
quellen werden zunehmen. Gleichzeitig steigt auch der Informations- und Beratungs-
bedarf der Unternehmen. Hier liegt auch für Verbände, Kammern und Institute ein in
Zukunft eher noch wichtiger werdendes Betätigungsfeld. Erforderlich sind auch Ände-
rungen bei den Unternehmen selbst. Durch eine Verbesserung der Eigenkapitalquote
können sie Bonität signalisieren und ihren Zugang zu Fremdkapital erleichtern.
Viele Unternehmen, gerade im Mittelstand, müssen auch ihre Beziehung zur Bank
auf eine neue Grundlage stellen. Sie müssen gegenüber den Kreditinstituten mehr
Transparenz und Offenheit schaffen. Die Kommunikation der eigenen Unterneh-
mensziele und -ergebnisse gegenüber den Finanzgebern wird im Hinblick auf das
Rating wichtiger als je zuvor – auch für kleinere Unternehmen.
Die vorliegende Untersuchung wirft ein detailliertes Licht auf die Veränderungen im
deutschen Finanzsektor. Sie soll der Standortbestimmung, aber auch der Überprü-
fung und Entwicklung von Strategien für alle Beteiligten dienen.
Um die unabdingbare Aktualität zu sichern und auch Fortschritte feststellen zu kön-
nen, beabsichtigen die beteiligten Verbände und die KfW diese Studie in jährlichem
Rhythmus zu wiederholen.
"""


if __name__ == "__main__":
    url = "https://de.wikipedia.org/wiki/Diotima"
    #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    text = text.replace("-\n", "")
    parser = PlaintextParser.from_string(string=text,tokenizer=Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    test = summarizer(parser.document, SENTENCES_COUNT)
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        sentence
        print(sentence)