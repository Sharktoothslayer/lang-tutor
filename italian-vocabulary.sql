-- Italian Vocabulary for Language Learning
-- This file contains common Italian words organized by difficulty level

-- Beginner Level (Level 1) - Basic words
INSERT INTO vocabulary (language_code, word, translation, part_of_speech, difficulty_level, example_sentence, pronunciation) VALUES
('it', 'ciao', 'hello/hi', 'interjection', 1, 'Ciao! Come stai?', 'chow'),
('it', 'grazie', 'thank you', 'interjection', 1, 'Grazie mille!', 'grah-tsee-eh'),
('it', 'prego', 'you''re welcome', 'interjection', 1, 'Prego, non c''è di che.', 'preh-go'),
('it', 'sì', 'yes', 'adverb', 1, 'Sì, capisco.', 'see'),
('it', 'no', 'no', 'adverb', 1, 'No, non lo so.', 'noh'),
('it', 'per favore', 'please', 'phrase', 1, 'Per favore, aiutatemi.', 'pehr fah-voh-reh'),
('it', 'scusa', 'sorry/excuse me', 'interjection', 1, 'Scusa, non capisco.', 'skoo-zah'),
('it', 'buongiorno', 'good morning', 'phrase', 1, 'Buongiorno! Come stai?', 'bwon-jor-noh'),
('it', 'buonasera', 'good evening', 'phrase', 1, 'Buonasera, signore.', 'bwon-ah-seh-rah'),
('it', 'buonanotte', 'good night', 'phrase', 1, 'Buonanotte, dormi bene.', 'bwon-ah-not-teh');

-- Beginner Level (Level 2) - Common nouns
INSERT INTO vocabulary (language_code, word, translation, part_of_speech, difficulty_level, example_sentence, pronunciation) VALUES
('it', 'acqua', 'water', 'noun', 2, 'Vorrei un bicchiere d''acqua.', 'ah-kwah'),
('it', 'pane', 'bread', 'noun', 2, 'Il pane è fresco.', 'pah-neh'),
('it', 'casa', 'house/home', 'noun', 2, 'La mia casa è grande.', 'kah-zah'),
('it', 'tempo', 'time/weather', 'noun', 2, 'Che tempo fa oggi?', 'tehm-poh'),
('it', 'uomo', 'man', 'noun', 2, 'L''uomo è alto.', 'woh-moh'),
('it', 'donna', 'woman', 'noun', 2, 'La donna è bella.', 'dohn-nah'),
('it', 'bambino', 'child', 'noun', 2, 'Il bambino gioca.', 'bam-bee-noh'),
('it', 'amico', 'friend', 'noun', 2, 'Il mio amico è simpatico.', 'ah-mee-koh'),
('it', 'lavoro', 'work/job', 'noun', 2, 'Il mio lavoro è interessante.', 'lah-voh-roh'),
('it', 'città', 'city', 'noun', 2, 'Roma è una bella città.', 'cheet-tah');

-- Intermediate Level (Level 3) - Verbs and adjectives
INSERT INTO vocabulary (language_code, word, translation, part_of_speech, difficulty_level, example_sentence, pronunciation) VALUES
('it', 'essere', 'to be', 'verb', 3, 'Io sono italiano.', 'ehs-seh-reh'),
('it', 'avere', 'to have', 'verb', 3, 'Ho una macchina.', 'ah-veh-reh'),
('it', 'fare', 'to do/make', 'verb', 3, 'Cosa fai oggi?', 'fah-reh'),
('it', 'andare', 'to go', 'verb', 3, 'Dove vai?', 'ahn-dah-reh'),
('it', 'venire', 'to come', 'verb', 3, 'Vieni qui, per favore.', 'veh-nee-reh'),
('it', 'bello', 'beautiful', 'adjective', 3, 'Che bella giornata!', 'behl-loh'),
('it', 'grande', 'big/large', 'adjective', 3, 'La casa è grande.', 'grahn-deh'),
('it', 'piccolo', 'small/little', 'adjective', 3, 'Il gatto è piccolo.', 'peek-koh-loh'),
('it', 'nuovo', 'new', 'adjective', 3, 'Ho comprato una macchina nuova.', 'nwoh-voh'),
('it', 'vecchio', 'old', 'adjective', 3, 'Il libro è vecchio.', 'vehk-kee-oh');

-- Intermediate Level (Level 4) - More complex words
INSERT INTO vocabulary (language_code, word, translation, part_of_speech, difficulty_level, example_sentence, pronunciation) VALUES
('it', 'ristorante', 'restaurant', 'noun', 4, 'Andiamo al ristorante.', 'rees-toh-rahn-teh'),
('it', 'università', 'university', 'noun', 4, 'Studio all''università.', 'oo-nee-vehr-see-tah'),
('it', 'teatro', 'theater', 'noun', 4, 'Il teatro è antico.', 'teh-ah-troh'),
('it', 'biblioteca', 'library', 'noun', 4, 'La biblioteca è aperta.', 'bee-blee-oh-teh-kah'),
('it', 'ospedale', 'hospital', 'noun', 4, 'L''ospedale è vicino.', 'ohs-peh-dah-leh'),
('it', 'stazione', 'station', 'noun', 4, 'La stazione è lontana.', 'stah-tsee-oh-neh'),
('it', 'aeroporto', 'airport', 'noun', 4, 'L''aeroporto è grande.', 'ah-eh-roh-por-toh'),
('it', 'supermercato', 'supermarket', 'noun', 4, 'Vado al supermercato.', 'soo-pehr-mehr-kah-toh'),
('it', 'farmacia', 'pharmacy', 'noun', 4, 'La farmacia è chiusa.', 'fahr-mah-chee-ah'),
('it', 'banca', 'bank', 'noun', 4, 'La banca è aperta.', 'bahn-kah');

-- Advanced Level (Level 5) - Complex expressions
INSERT INTO vocabulary (language_code, word, translation, part_of_speech, difficulty_level, example_sentence, pronunciation) VALUES
('it', 'capire', 'to understand', 'verb', 5, 'Capisco quello che dici.', 'kah-pee-reh'),
('it', 'pensare', 'to think', 'verb', 5, 'Penso che sia giusto.', 'pehn-sah-reh'),
('it', 'sapere', 'to know', 'verb', 5, 'So dove abiti.', 'sah-peh-reh'),
('it', 'volere', 'to want', 'verb', 5, 'Voglio imparare l''italiano.', 'voh-leh-reh'),
('it', 'potere', 'can/be able to', 'verb', 5, 'Posso aiutarti.', 'poh-teh-reh'),
('it', 'dovere', 'must/have to', 'verb', 5, 'Devo studiare.', 'doh-veh-reh'),
('it', 'piacere', 'to like', 'verb', 5, 'Mi piace la musica.', 'pee-ah-cheh-reh'),
('it', 'interessante', 'interesting', 'adjective', 5, 'Il film è interessante.', 'een-teh-rehs-sahn-teh'),
('it', 'difficile', 'difficult', 'adjective', 5, 'L''italiano è difficile.', 'deef-fee-chee-leh'),
('it', 'facile', 'easy', 'adjective', 5, 'È facile da capire.', 'fah-chee-leh');

-- Common phrases and expressions
INSERT INTO vocabulary (language_code, word, translation, part_of_speech, difficulty_level, example_sentence, pronunciation) VALUES
('it', 'come stai', 'how are you', 'phrase', 2, 'Ciao! Come stai?', 'koh-meh stah-ee'),
('it', 'mi chiamo', 'my name is', 'phrase', 2, 'Mi chiamo Marco.', 'mee kee-ah-moh'),
('it', 'piacere di conoscerti', 'nice to meet you', 'phrase', 3, 'Piacere di conoscerti!', 'pee-ah-cheh-reh dee koh-noh-shehr-tee'),
('it', 'dove abiti', 'where do you live', 'phrase', 3, 'Dove abiti?', 'doh-veh ah-bee-tee'),
('it', 'cosa fai', 'what do you do', 'phrase', 3, 'Cosa fai nella vita?', 'koh-sah fah-ee'),
('it', 'non capisco', 'I don''t understand', 'phrase', 2, 'Mi dispiace, non capisco.', 'nohn kahm-pees-koh'),
('it', 'puoi ripetere', 'can you repeat', 'phrase', 3, 'Puoi ripetere, per favore?', 'pwoh-ee ree-peh-teh-reh'),
('it', 'parli inglese', 'do you speak English', 'phrase', 3, 'Parli inglese?', 'pahr-lee een-gleh-seh'),
('it', 'quanto costa', 'how much does it cost', 'phrase', 4, 'Quanto costa questo?', 'kwahn-toh kohs-tah'),
('it', 'a che ora', 'at what time', 'phrase', 4, 'A che ora inizia il film?', 'ah keh oh-rah');
