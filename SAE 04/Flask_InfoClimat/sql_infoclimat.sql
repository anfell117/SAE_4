DROP TABLE IF EXISTS participer;
DROP TABLE IF EXISTS animer;
DROP TABLE IF EXISTS s_occuper;
DROP TABLE IF EXISTS former;
DROP TABLE IF EXISTS travailler;
DROP TABLE IF EXISTS se_situer;

DROP TABLE IF EXISTS participant;
DROP TABLE IF EXISTS animation;
DROP TABLE IF EXISTS animateur;
DROP TABLE IF EXISTS atelier;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS formateur;
DROP TABLE IF EXISTS ville;
DROP TABLE IF EXISTS profession;


CREATE TABLE atelier(
                        id_atelier INT AUTO_INCREMENT,
                        nom_atelier VARCHAR(50),
                        theme_atelier VARCHAR(50),
                        PRIMARY KEY(id_atelier)
);

CREATE TABLE adresse(
                        id_adresse INT AUTO_INCREMENT,
                        nom_rue VARCHAR(50),
                        numero_rue INT,
                        PRIMARY KEY(id_adresse)
);

CREATE TABLE formateur(
                          id_formateur INT AUTO_INCREMENT,
                          nom_formateur VARCHAR(50),
                          prenom_formateur VARCHAR(50),
                          PRIMARY KEY(id_formateur)
);

CREATE TABLE profession(
                           id_profession INT AUTO_INCREMENT,
                           nom_profession VARCHAR(50),
                           PRIMARY KEY(id_profession)
);

CREATE TABLE ville(
                      id_ville INT AUTO_INCREMENT,
                      nom_ville VARCHAR(50),
                      code_postal VARCHAR(50),
                      PRIMARY KEY(id_ville)
);

CREATE TABLE animateur(
                          id_animateur INT AUTO_INCREMENT,
                          nom_animateur VARCHAR(50),
                          prenom_animateur VARCHAR(50),
                          telephone_animateur VARCHAR(50),
                          disponibilité BOOLEAN,
                          adresse_id INT NOT NULL,
                          PRIMARY KEY(id_animateur),
                          FOREIGN KEY(adresse_id) REFERENCES adresse(id_adresse)
);

CREATE TABLE animation(
                          id_animation INT AUTO_INCREMENT,
                          nom_animation VARCHAR(50),
                          nb_places_disponibles VARCHAR(50),
                          date_animation DATE,
                          atelier_id INT NOT NULL,
                          adresse_id INT NOT NULL,
                          PRIMARY KEY(id_animation),
                          FOREIGN KEY(atelier_id) REFERENCES atelier(id_atelier),
                          FOREIGN KEY(adresse_id) REFERENCES adresse(id_adresse)
);

CREATE TABLE participant(
                            id_participant INT AUTO_INCREMENT,
                            prenom_participant VARCHAR(50),
                            nom_participant VARCHAR(50),
                            adresse_mail_participant VARCHAR(50),
                            telephone VARCHAR(50),
                            present BOOLEAN,
                            adresse_id INT NOT NULL,
                            PRIMARY KEY(id_participant),
                            FOREIGN KEY(adresse_id) REFERENCES adresse(id_adresse)
);

CREATE TABLE animer(
                       animateur_id INT,
                       animation_id INT,
                       PRIMARY KEY(animateur_id, animation_id),
                       FOREIGN KEY(animateur_id) REFERENCES animateur(id_animateur),
                       FOREIGN KEY(animation_id) REFERENCES animation(id_animation)
);

CREATE TABLE participer(
                           animation_id INT,
                           participant_id INT,
                           note_animateur VARCHAR(50),
                           nb_present INT,
                           note_atelier VARCHAR(50),
                           PRIMARY KEY(animation_id, participant_id),
                           FOREIGN KEY(animation_id) REFERENCES animation(id_animation),
                           FOREIGN KEY(participant_id) REFERENCES participant(id_participant)
);

CREATE TABLE s_occuper(
                          animateur_id INT,
                          atelier_id INT,
                          PRIMARY KEY(animateur_id, atelier_id),
                          FOREIGN KEY(animateur_id) REFERENCES animateur(id_animateur),
                          FOREIGN KEY(atelier_id) REFERENCES atelier(id_atelier)
);

CREATE TABLE former(
                       animateur_id INT,
                       formateur_id INT,
                       PRIMARY KEY(animateur_id, formateur_id),
                       FOREIGN KEY(animateur_id) REFERENCES animateur(id_animateur),
                       FOREIGN KEY(formateur_id) REFERENCES formateur(id_formateur)
);

CREATE TABLE travailler(
                           animateur_id INT,
                           profession_id INT,
                           PRIMARY KEY(animateur_id, profession_id),
                           FOREIGN KEY(animateur_id) REFERENCES animateur(id_animateur),
                           FOREIGN KEY(profession_id) REFERENCES profession(id_profession)
);

CREATE TABLE se_situer(
                          adresse_id INT,
                          ville_id INT,
                          PRIMARY KEY(adresse_id, ville_id),
                          FOREIGN KEY(adresse_id) REFERENCES adresse(id_adresse),
                          FOREIGN KEY(ville_id) REFERENCES ville(id_ville)
);

-- INSERTIONS
INSERT INTO atelier VALUES
                        (NULL, 'Comprendre le réchauffement climatique', 'Changement climatique'),
                        (NULL, 'Réduire son empreinte carbone', 'Écologie'),
                        (NULL, 'Le recyclage au quotidien', 'Gestion des déchets'),
                        (NULL, 'Protéger la biodiversité', 'Environnement');

INSERT INTO adresse VALUES
                                              (NULL, 'Rue de la République', 12),
                                              (NULL, 'Rue des Écoles', 25),
                                              (NULL, 'Avenue de la Gare', 8);

INSERT INTO formateur VALUES
                          (NULL,'KOKIC', 'Daris'),
                          (NULL, 'DERARDJA', 'Anfel'),
                          (NULL, 'CHELLAH', 'Ilias');

INSERT INTO profession VALUES
                           (NULL, 'Professeur'),
                           (NULL, 'Agriculteur/Agricultrice'),
                           (NULL, 'Medecin');

INSERT INTO ville VALUES
                                               (NULL, 'Besançon', '25000'),
                                               (NULL, 'Dijon', '21000'),
                                               (NULL, 'Dole', '39100');

INSERT INTO animateur VALUES
    (NULL, 'Cailloux', 'Lana', '0612345678', TRUE, 1),
    (NULL, 'Mangeur', 'Tom', '0623456789', TRUE, 2),
    (NULL, 'LaChaise', 'Noa', '0634567890', FALSE, 3);


INSERT INTO animation VALUES
                          (NULL, 'Conférence sur le climat', '30', '2026-12-01', 1, 1),
                          (NULL, 'Défi zéro carbone', '20', '2026-12-03', 2, 2),
                          (NULL, 'Atelier fabrication de produits recyclés', '15', '2026-12-05', 3, 3);



INSERT INTO participant VALUES
    (NULL, 'Quentin', 'LaSalle', 'alice.robert@example.com', '0611111111', TRUE, 1),
    (NULL, 'Néperian', 'Logarithme', 'lucas.petit@example.com', '0622222222', TRUE, 2),
    (NULL, 'Pi', 'Racine', 'emma.laurent@example.com', '0633333333', TRUE, 3);

INSERT INTO animer VALUES
                       (1, 1),
                       (2, 2),
                       (3, 3);

INSERT INTO participer VALUES
    (1, 1, 'Professionnel, très bien!', 1, 'Très intéressant'),
    (1, 2, 'Explique bien.', 1, 'Très instructif'),
    (1, 3, 'Pas très investi.', 1, 'Moyen');

INSERT INTO s_occuper VALUES
                          (1, 1),
                          (2, 2),
                          (3, 3);

INSERT INTO former VALUES
                       (1, 1),
                       (2, 2),
                       (3, 3);

INSERT INTO travailler VALUES
                           (1, 1),
                           (2, 2),
                           (3, 3);

INSERT INTO se_situer VALUES
                          (1, 1),
                          (2, 1),
                          (3, 1);


-- Requêtes

SELECT animateur.nom_animateur, animateur.prenom_animateur, COUNT(animer.animation_id) AS nombre_animations
FROM animateur
JOIN animer ON animateur.id_animateur = animer.animateur_id
GROUP BY animateur.id_animateur, animateur.nom_animateur, animateur.prenom_animateur
ORDER BY nombre_animations DESC;


SELECT participant.nom_participant, participant.prenom_participant
FROM participant
JOIN participer ON participant.id_participant = participer.participant_id
ORDER BY participant.nom_participant ASC;


SELECT animateur.nom_animateur, animateur.prenom_animateur, profession.nom_profession
FROM animateur
JOIN travailler ON animateur.id_animateur = travailler.animateur_id
JOIN profession ON travailler.profession_id = profession.id_profession
ORDER BY animateur.nom_animateur ASC;

