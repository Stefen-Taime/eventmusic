subjects=$(curl -X GET http://localhost:8081/subjects)

subjects_array=($(echo $subjects | tr ',' '\n'))

for subject in "${subjects_array[@]}"
do
    subject_cleaned=$(echo $subject | tr -d '[]"')
    echo "Suppression des schémas pour le sujet: $subject_cleaned"
    curl -X DELETE http://localhost:8081/subjects/$subject_cleaned
done
