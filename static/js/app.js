$('form input[type="file"]').change(event => {
  let archivos = event.target.files;
  if (archivos.length == 0) {
    console.log('sin imagen para mostrar')
  } else {
      if(archivos[0].type == 'image/jpeg') {
        $('img').remove();
        let imagen = $('<img class="img-responsive" width="400" >');
        imagen.attr('src', window.URL.createObjectURL(archivos[0]));
        $('figure').prepend(imagen);
      } else {
          alert('Formato no soportado, solo acepta .JPG ó .JPEG')
      }
  }
});


$("#btnSubirFoto").click(function(){
    //... carga texto: Detectando objeto ...
    var textoDetectaId="Detectando objeto en la imagen ..."
    let textoDetectado =$('<p id="textoDetecta"></p>')
    textoDetectado.text(textoDetectaId)
    //$('picture').prepend(textoDetectado);
    
    //... carga GIF circulo espera ...
    var detectaId ="./static/img/procesando.gif"
    let detectado = $('<img id="detecta" width="150" height="150">');
    detectado.attr('src',detectaId);    
    $('picture').prepend(detectado, textoDetectado); 
});