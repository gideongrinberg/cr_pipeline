SELECT * into mydb.MyTable_0 from CatalogRecord
WHERE objType = 'STAR'
  AND Tmag BETWEEN 0 AND 16
  AND lumclass = 'DWARF'
  AND d BETWEEN 1 AND 150
  AND (gaiabp - gaiarp) > 1.5
  AND (GAIAmag + 5 * LOG10(d) + 5) > 4