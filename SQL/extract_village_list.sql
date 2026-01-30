SELECT
    vl.village_moo,
    CONCAT(LEFT(vl.village_name, 3), '****') AS village_name_mask,
    CONCAT('****', RIGHT(ta.full_name, 10)) AS full_name_mask
FROM village vl
LEFT JOIN thaiaddress ta
    ON ta.addressid = vl.address_id;
