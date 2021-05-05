DROP TABLE IF EXISTS BookTags;
DROP TABLE IF EXISTS BookRecipes;
DROP TABLE IF EXISTS RecipeTags;
DROP TABLE IF EXISTS RecipeIngredients;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Ingredients;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Steps;
DROP TABLE IF EXISTS Recipes;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users(
  UserID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(40) NOT NULL,
  PasswordHash VARCHAR(64) NOT NULL,
  Role VARCHAR(40) NOT NULL,

  PRIMARY KEY (UserID),
  UNIQUE (Name)
);

CREATE TABLE Recipes(
  RecipeID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(40) NOT NULL,
  ActiveTimeMinutes INT,
  TotalTimeMinutes INT,
  Description VARCHAR(300),
  Servings INT,
  UserID INT NOT NULL,

  PRIMARY KEY (RecipeID),
  FOREIGN KEY (UserID) REFERENCES Users(UserID)
	ON DELETE CASCADE
);

CREATE TABLE Steps(
  RecipeID INT NOT NULL,
  Ordinal INT NOT NULL,
  Instructions VARCHAR(200) NOT NULL,

  PRIMARY KEY (Ordinal, RecipeID),
  FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID)
	ON DELETE CASCADE
);

CREATE TABLE Books(
  BookID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(40) NOT NULL,

  PRIMARY KEY (BookID)
);

CREATE TABLE Ingredients(
  IngredientID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(40) NOT NULL,

  PRIMARY KEY (IngredientID)
);

CREATE TABLE Tags(
  TagID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(40) NOT NULL,

  PRIMARY KEY (TagID)
);

CREATE TABLE RecipeIngredients(
  RecipeID INT NOT NULL,
  IngredientID INT NOT NULL,
  Amount FLOAT,
  Unit VARCHAR(10),

  PRIMARY KEY (RecipeID, IngredientID),
  FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID)
	ON DELETE CASCADE,
  FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID)
	ON DELETE CASCADE
);

CREATE TABLE RecipeTags(
  RecipeID INT NOT NULL,
  TagID INT NOT NULL,

  PRIMARY KEY (RecipeID, TagID),
  FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID)
	ON DELETE CASCADE,
  FOREIGN KEY (TagID) REFERENCES Tags(TagID)
	ON DELETE CASCADE
);

CREATE TABLE BookRecipes(
  BookID INT NOT NULL,
  RecipeID INT NOT NULL,

  PRIMARY KEY (RecipeID, BookID),
  FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID)
	ON DELETE CASCADE,
  FOREIGN KEY (BookID) REFERENCES Books(BookID)
	ON DELETE CASCADE
);

CREATE TABLE BookTags(
  BookID INT NOT NULL,
  TagID INT NOT NULL,

  PRIMARY KEY (TagID, BookID),
  FOREIGN KEY (TagID) REFERENCES Tags(TagID)
	ON DELETE CASCADE,
  FOREIGN KEY (BookID) REFERENCES Books(BookID)
	ON DELETE CASCADE
);