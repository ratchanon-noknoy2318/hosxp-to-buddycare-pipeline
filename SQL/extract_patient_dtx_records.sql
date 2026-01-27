SELECT
    p.hn,
    p.cid,
    p.pname,
    p.fname,
    p.lname,
    p.sex,
    CASE p.sex
        WHEN 1 THEN 'ชาย'
        WHEN 2 THEN 'หญิง'
        ELSE 'ไม่ระบุ'
    END AS sex_name
FROM
    patient p
WHERE
    (
        p.sex = 1 AND p.pname IN ('นาง', 'นางสาว')
        OR
        p.sex = 2 AND p.pname = 'นาย'and   p.death = 'N'
    )

