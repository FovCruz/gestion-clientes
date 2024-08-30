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
        dots: false,
        pauseOnHover: false,
        adaptiveHeight: true
    });
});
