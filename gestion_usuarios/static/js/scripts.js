// LOGO CARRUSEL
$(document).ready(function () {
    $('.logo-carrusel').slick({
        slidesToShow: 7,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 1000, // Cambiado a 2000ms para una rotación continua
        arrows: false,
        dots: false,
        pauseOnHover: false,
        infinite: true, // Asegura que el carrusel sea infinito
        speed: 1000, // Añadido para una transición suave
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 4
                }
            },
            {
                breakpoint: 520,
                settings: {
                    slidesToShow: 3
                }
            }
        ]
    });
});

//SLIDER HOME 
$(document).ready(function () {
    $('.banner-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        arrows: true,
        dots: true,
        pauseOnHover: false,
        adaptiveHeight: true,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    arrows: false, // Ocultar los botones en dispositivos móviles
                    dots: true
                }
            }
        ]
    });
});

// FORMATEAR VALORES
document.addEventListener("DOMContentLoaded", function() {
    function formatPrice(price) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    document.querySelectorAll('.price').forEach(function(priceElement) {
        let priceText = priceElement.textContent.trim().replace("CLP ", "").replace(",", "");
        let formattedPrice = formatPrice(parseFloat(priceText));
        priceElement.textContent = `Precio $ ${formattedPrice}`;
    });
});

//CONFIRMACION & EXITO ELIMINAR USUARIO
  // Pasar los datos del usuario al modal de confirmación de eliminación
  $('#deleteModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Botón que disparó el modal
    var userId = button.data('id'); // Extraer el ID del usuario
    var userName = button.data('nombre') + ' ' + button.data('apellido'); // Extraer el nombre del usuario
    
    var modal = $(this);
    modal.find('#deleteUserName').text(userName); // Mostrar el nombre del usuario en el modal
    modal.find('#confirmDeleteButton').data('id', userId); // Asignar el ID del usuario al botón de confirmación
});

// Manejar la confirmación de eliminación
$('#confirmDeleteButton').on('click', function () {
    var userId = $(this).data('id'); // Obtener el ID del usuario
    var url = '/usuarios/eliminar/' + userId + '/'; // Construir la URL de eliminación

    // Obtener el token CSRF del formulario
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); 

    // Hacer la petición para eliminar al usuario
    $.ajax({
        url: url,
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken }, // Incluye el token CSRF en los headers
        data: {
            _method: 'DELETE', // Especificar que se trata de una eliminación
        },
        success: function () {
            $('#deleteModal').modal('hide'); // Cerrar el modal de confirmación
            $('#successModal').modal('show'); // Mostrar el modal de éxito

            // Opcional: recargar la página después de un breve retardo
            setTimeout(function(){
                location.reload();
            }, 2000);
        },
        error: function () {
            alert('Error al eliminar el usuario. Por favor, inténtalo de nuevo porfis.');
        }
    });
});