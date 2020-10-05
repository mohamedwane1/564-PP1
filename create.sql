drop table if exists Items;
drop table if exists Users;
drop table if exists Bids;
drop table if exists Categories;

CREATE TABLE Items
(
    ItemID INT NOT NULL,
    Name VARCHAR NOT NULL,
    Currently FLOAT NOT NULL,
    Buy_Price FLOAT,
    First_Bid FLOAT NOT NULL,
    Number_of_Bids INT NOT NULL,
    Started VARCHAR NOT NULL,
    Ends VARCHAR NOT NULL,
    Description VARCHAR NOT NULL,
    UserID VARCHAR NOT NULL,
    Categories INT NOT NULL,
    PRIMARY KEY(ItemID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Users
(
    UserID VARCHAR NOT NULL,
    ItemID INT NOT NULL,
    Rating INT NOT NULL,
    Location VARCHAR,
    Country VARCHAR,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Bids
(
    UserID VARCHAR NOT NULL,
    ItemID INT NOT NULL,
    Amount INT NOT NULL,
    Time VARCHAR NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Categories
(
    ItemID INT NOT NULL,
    Category VARCHAR,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);
