let datatable;
let dataTableIsInitialized = false;

const options = {
  columnsDefs: [
    { className: 'centered', targets: [0, 1, 2, 3, 4] },
    { orderrable: false, target: [4] },
    { searchable: false, targets: [0, 1, 2, 3] },
  ],
  pageLength: 4,
  destroy: true,
};

const initDataTable = async () => {
  if (dataTableIsInitialized) {
    datatable.destroy();
  }
  await listProducts();
  datatable = $('#datatable_products').DataTable(options);
  dataTableIsInitialized = true;
  $(document).ready(function () {
    $('[data-bs-toggle="modal"]').modal();
  });
};

const listProducts = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/list_products');
    const data = await response.json();
    let content = '';
    data.products.forEach((product, index) => {
      content += `
        <tr>
          <td>${product.sku}</td>
          <td>${product.name}</td>
          <td>${product.price}</td>
          <td>${product.brand}</td>
          <td>
          <button class="btn btn-primary"  onclick="redirectToEditPage(${product.id})">Editar</button>
            <button class="btn btn-danger" onclick="deleteProduct(${product.id})">Eliminar</button>
          </td>
        </tr>
        `;
    });
    $('#datatable_products tbody').html(content); // Actualizar el contenido de la tabla
    console.log(data);
  } catch (error) {
    console.log('Error:', error);
  }
};


function redirectToEditPage(productId) {
  window.location.href = `/editar_producto/${productId}`
}

const deleteProduct = (productId) => {
  fetch(`/delete_product/${productId}`, {
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
window.addEventListener('load', async () => {
  await initDataTable();
});
