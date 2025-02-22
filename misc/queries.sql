--- Create targets.csv from TIC parquets. --- 
CREATE TABLE targets AS
    SELECT * FROM read_parquet("./misc/targets/*.parquet");

COPY (SELECT ID, ra, dec FROM targets) TO "./misc/targets/targets.csv";

--- Check completeness --- 
CREATE TABLE known_crs AS 
    SELECT TICID FROM read_csv("./tests/data/complex/*.csv", union_by_name=true);

CREATE TABLE targets AS FROM "./misc/targets_full.parquet";

CREATE TABLE missing AS
SELECT * FROM known_crs
WHERE known_crs.TICID NOT IN (SELECT ID FROM targets);

ALTER TABLE missing RENAME COLUMN TICID to ID;
COPY missing TO "missing.csv";

--- Get list of known_crs with RA and Dec for testing purposes ---
CREATE TABLE crs_full AS
SELECT known_crs.TICID, targets.ra, targets.dec 
FROM known_crs INNER JOIN targets 
ON known_crs.TICID = targets.ID; 

