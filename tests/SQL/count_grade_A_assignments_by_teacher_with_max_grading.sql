WITH TeacherGradedAssignments AS (
    SELECT 
        teacher_id,
        COUNT(*) AS total_graded
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        teacher_id
    ORDER BY 
        total_graded DESC
    LIMIT 1
),
GradeACount AS (
    SELECT 
        teacher_id,
        COUNT(*) AS grade_a_count
    FROM 
        assignments
    WHERE 
        grade = 'A'
    GROUP BY 
        teacher_id
)
SELECT 
    g.grade_a_count
FROM 
    TeacherGradedAssignments t
JOIN 
    GradeACount g ON t.teacher_id = g.teacher_id;
