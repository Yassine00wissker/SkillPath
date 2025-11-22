-- SkillPath Database Dummy Data
-- Generated SQL script to populate the database with sample data

USE skillpath;

-- Clear existing data (optional - comment out if you want to keep existing data)
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE parcours;
-- TRUNCATE TABLE formations;
-- TRUNCATE TABLE categories;
-- TRUNCATE TABLE users;
-- TRUNCATE TABLE admins;
-- SET FOREIGN_KEY_CHECKS = 1;

-- Insert Admin
INSERT INTO admins (nom, prenom, email, password) VALUES
('Admin', 'System', 'admin@skillpath.com', '$2b$12$2ddIZQsA5ecrnQVLaOp.FuGictdJQLcWYSG3iuajY532LlB2157w6'),
('Dupont', 'Jean', 'jean.dupont@skillpath.com', '$2b$12$2ddIZQsA5ecrnQVLaOp.FuGictdJQLcWYSG3iuajY532LlB2157w6');

-- Insert Categories
INSERT INTO categories (nom) VALUES
('Développement Web'),
('Développement Mobile'),
('Data Science'),
('Cybersécurité'),
('Design'),
('Marketing Digital'),
('Gestion de Projet'),
('Intelligence Artificielle');

-- Insert Users with competences and interests
INSERT INTO users (nom, prenom, email, competence, interests, password) VALUES
('Martin', 'Sophie', 'sophie.martin@email.com', 
 '["python", "fastapi", "sql", "javascript"]', 
 '["web development", "backend", "api design"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS'),

('Bernard', 'Pierre', 'pierre.bernard@email.com', 
 '["javascript", "react", "node.js", "css"]', 
 '["frontend", "ui/ux", "web development"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS'),

('Dubois', 'Marie', 'marie.dubois@email.com', 
 '["python", "sql", "excel", "data analysis"]', 
 '["data science", "analytics", "machine learning"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS'),

('Thomas', 'Lucas', 'lucas.thomas@email.com', 
 '["java", "spring", "sql", "docker"]', 
 '["backend", "microservices", "devops"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS'),

('Robert', 'Emma', 'emma.robert@email.com', 
 '["python", "tensorflow", "pytorch", "sql"]', 
 '["machine learning", "ai", "deep learning"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS'),

('Petit', 'Antoine', 'antoine.petit@email.com', 
 '["javascript", "react", "typescript", "node.js"]', 
 '["fullstack", "web development", "frontend"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS'),

('Durand', 'Camille', 'camille.durand@email.com', 
 '["python", "django", "postgresql", "redis"]', 
 '["backend", "web development", "api"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS'),

('Leroy', 'Julien', 'julien.leroy@email.com', 
 '["sql", "excel", "power bi", "python"]', 
 '["data analysis", "business intelligence", "analytics"]', 
 '$2b$12$a094Xa7PM3qNo2NhJd.8oOgJHpB3u9wnYluE4e5.0h0ByJesOojrS');

-- Insert Formations
INSERT INTO formations (titre, description, video, category_id) VALUES
('Introduction à Python', 
 'Apprenez les bases de Python : syntaxe, structures de données, fonctions et programmation orientée objet. Parfait pour débutants.',
 'https://example.com/videos/python-intro.mp4', 
 1),

('FastAPI : Créer des APIs Modernes', 
 'Maîtrisez FastAPI pour créer des APIs RESTful performantes avec validation automatique, documentation interactive et support asynchrone.',
 'https://example.com/videos/fastapi-tutorial.mp4', 
 1),

('React : Développement Frontend Moderne', 
 'Découvrez React, la bibliothèque JavaScript pour créer des interfaces utilisateur interactives et réactives.',
 'https://example.com/videos/react-course.mp4', 
 1),

('JavaScript Avancé', 
 'Approfondissez vos connaissances en JavaScript : closures, promises, async/await, et patterns avancés.',
 'https://example.com/videos/js-advanced.mp4', 
 1),

('Développement Mobile avec React Native', 
 'Créez des applications mobiles cross-platform avec React Native pour iOS et Android.',
 'https://example.com/videos/react-native.mp4', 
 2),

('Flutter : Applications Mobiles', 
 'Développez des applications mobiles natives avec Flutter et Dart.',
 'https://example.com/videos/flutter-course.mp4', 
 2),

('Data Science avec Python', 
 'Analysez des données avec pandas, numpy, matplotlib et scikit-learn. De la manipulation à la visualisation.',
 'https://example.com/videos/data-science-python.mp4', 
 3),

('SQL pour l''Analyse de Données', 
 'Maîtrisez SQL pour interroger et analyser des bases de données relationnelles efficacement.',
 'https://example.com/videos/sql-analysis.mp4', 
 3),

('Machine Learning Fondamentaux', 
 'Introduction au machine learning : algorithmes supervisés et non supervisés, évaluation de modèles.',
 'https://example.com/videos/ml-fundamentals.mp4', 
 3),

('Sécurité Web : OWASP Top 10', 
 'Comprenez et protégez-vous contre les 10 vulnérabilités web les plus critiques selon OWASP.',
 'https://example.com/videos/owasp-security.mp4', 
 4),

('Ethical Hacking', 
 'Apprenez les techniques de test d''intrusion et de sécurisation des systèmes.',
 'https://example.com/videos/ethical-hacking.mp4', 
 4),

('UI/UX Design Principles', 
 'Les fondamentaux du design d''interface utilisateur et de l''expérience utilisateur.',
 'https://example.com/videos/ui-ux-design.mp4', 
 5),

('Figma : Design d''Interfaces', 
 'Créez des prototypes et designs d''interfaces avec Figma.',
 'https://example.com/videos/figma-tutorial.mp4', 
 5),

('Marketing Digital : Stratégies', 
 'Développez votre présence en ligne avec les techniques de marketing digital modernes.',
 'https://example.com/videos/digital-marketing.mp4', 
 6),

('SEO et Référencement', 
 'Optimisez votre site web pour les moteurs de recherche et augmentez votre visibilité.',
 'https://example.com/videos/seo-course.mp4', 
 6),

('Gestion de Projet Agile', 
 'Maîtrisez les méthodologies Agile (Scrum, Kanban) pour gérer vos projets efficacement.',
 'https://example.com/videos/agile-project-management.mp4', 
 7),

('Deep Learning avec TensorFlow', 
 'Créez des réseaux de neurones profonds avec TensorFlow pour résoudre des problèmes complexes.',
 'https://example.com/videos/tensorflow-deep-learning.mp4', 
 8),

('NLP : Traitement du Langage Naturel', 
 'Apprenez à traiter et analyser le langage naturel avec Python et les bibliothèques modernes.',
 'https://example.com/videos/nlp-course.mp4', 
 8);

-- Insert Parcours (Learning Paths)
INSERT INTO parcours (titre, description, listedeformations) VALUES
('Développeur Full Stack Python', 
 'Parcours complet pour devenir développeur full stack avec Python, FastAPI et React.',
 '[1, 2, 3, 4]'),

('Data Scientist', 
 'Formation complète en data science : de l''analyse de données au machine learning.',
 '[7, 8, 9]'),

('Développeur Mobile', 
 'Apprenez à créer des applications mobiles avec React Native et Flutter.',
 '[5, 6]'),

('Expert en Cybersécurité', 
 'Parcours complet pour devenir expert en sécurité informatique.',
 '[10, 11]'),

('Designer UI/UX', 
 'Formation complète en design d''interface et expérience utilisateur.',
 '[12, 13]'),

('Spécialiste Marketing Digital', 
 'Maîtrisez tous les aspects du marketing digital et du référencement.',
 '[14, 15]'),

('Ingénieur Machine Learning', 
 'Parcours avancé en intelligence artificielle et machine learning.',
 '[7, 9, 17, 18]'),

('Chef de Projet Tech', 
 'Formation complète en gestion de projet pour le secteur technologique.',
 '[1, 2, 16]');

-- Verify the data
SELECT 'Admins inserted:' as info, COUNT(*) as count FROM admins
UNION ALL
SELECT 'Users inserted:', COUNT(*) FROM users
UNION ALL
SELECT 'Categories inserted:', COUNT(*) FROM categories
UNION ALL
SELECT 'Formations inserted:', COUNT(*) FROM formations
UNION ALL
SELECT 'Parcours inserted:', COUNT(*) FROM parcours;
