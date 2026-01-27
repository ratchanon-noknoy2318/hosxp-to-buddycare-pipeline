SELECT ovst.hn,ovst.vsttime,ovst.spclty,
concat(patient.fname,' ',patient.lname) as patient_name, patient.birthday , spclty.name
FROM ovst
LEFT OUTER JOIN patient on patient.hn=ovst.hn
LEFT OUTER JOIN spclty on spclty.spclty=ovst.spclty
WHERE ovst.vstdate = '2025-06-20'
ORDER BY spclty.name