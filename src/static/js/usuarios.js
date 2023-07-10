let datatable;
let dataTableIsInitialized = false;

const options = {
  columnsDefs: [
    { className: "centered", targets: [0, 1, 2, 3,] },
    { orderrable: false, target: [1] },
    { searchable: false, targets: [0, 1] },
  ],
  pageLength: 4,
  destroy: true,
};

const initDataTable = async () => {
  if (dataTableIsInitialized) {
    datatable.destroy();
  }
  await listUsers();
  dataTable = $("#datatable_users").DataTable({});
  dataTableIsInitialized = true;
};

    const listUsers = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/list_users");
            const data = await response.json();
            console.log(data)
            let content = ``;
            data.users.forEach((user, index) => {
               
                 content += `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>
                    <button class="btn btn-primary"  onclick="redirectToEditPage(${user.id})">Editar</button>
                    <button class="btn btn-danger" onclick="deleteProduct(${user.id})">Eliminar</button>
                    </button>
                    </td>
                </tr>
                `;
            });
            $("#datatable_users tbody").html(content); // Actualizar el contenido de la tabla
            console.log(data);
        } catch (error) {
            console.log("error:", error);
        }
    };

    window.addEventListener("load", async () => {
    await initDataTable();
    await listUsers();
    });

    function redirectToEditPage(id) {
      window.location.href = `/editar_usuario/${id}`
    }
    
    const deleteProduct = (id) => {
      fetch(`/delete_user/${id}`, {
        method: 'DELETE',
      })
        .then((response) => {
          if (response.status === 405) {
            console.log(response);
            // Recargar la página si se recibe una respuesta con código de estado 302
            window.location.reload();
          } else if (response.ok) {
            console.log(response);
            // La eliminación se realizó correctamente, redirigir al usuario a la página de inicio o a otra página deseada
            window.location.href = '/index';  // Redirigir a la página de inicio
          } else {
            // Ocurrió un error al eliminar el producto
            console.log('Error al eliminar el producto');
          }
        })
        .catch((error) => {
          console.log('Error:', error);
        });
    };
function deleteUser(userId) {
  // Aquí puedes implementar la lógica para eliminar el usuario correspondiente al userId.
  console.log(`Eliminar usuario con ID: ${userId}`);
}
