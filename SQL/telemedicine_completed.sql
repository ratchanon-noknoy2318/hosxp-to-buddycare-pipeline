SELECT o.hn, CONCAT(p.pname, p.fname, ' ', p.lname) AS full_name, o.vstdate, vnstat.age_y, pt.name, ic.tname, vnstat.income
FROM ovst o
    LEFT JOIN patient p ON o.hn = p.hn
    LEFT JOIN opitemrece oi ON o.vn = oi.vn
    LEFT JOIN nondrugitems nd ON oi.icode = nd.icode
    left join vn_stat vnstat on vnstat.vn = o.vn
    left join pttype pt on pt.pttype = vnstat.pttype
    left join icd101 ic on vnstat.pdx = ic.code
where oi.icode = '3003921' and o.vstdate between '2025-01-01' and '2025-06-16'
order by o.vstdate