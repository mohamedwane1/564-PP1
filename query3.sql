SELECT COUNT(*) FROM (SELECT COUNT(Category) AS count FROM Categories GROUP BY ItemID) C WHERE count = 4