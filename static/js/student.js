async function getStudents() {

    try {

        const response = await fetch(
            "http://127.0.0.1:114/api/students/"
        );

        const data = await response.json();

        let output = "";

        data.forEach(student => {

            output += `
                <tr>
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.age}</td>
                    <td>${student.gender}</td>
                    <td>${student.percentage}</td>
                </tr>
            `;
        });

        document.getElementById("student-data").innerHTML = output;

    }
    catch(error) {

        console.log(error);

    }
}

getStudents();