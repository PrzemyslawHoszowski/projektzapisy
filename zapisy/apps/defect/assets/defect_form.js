// The following code is responsible for management of defect form and images formset

import "jquery";
const $ = jQuery;

let formsetCounter = 0;
let maxFormsetNumber = 0;
let extraImagesNumber = 0;

// List of positions of empty image forms that are available
// to add to the formset as new image forms. If list contains
// number n, it means, that the nth form from the top is
// available. List is in ascending order.
const listOfEmpty = [];


function newImageClick(event) {
  event.preventDefault();
  if (formsetCounter === maxFormsetNumber) return;

  if (!listOfEmpty) return;

  formsetCounter += 1;

  // We choose position of the first empty image form and remove it from
  // listOfEmpty.
  const first = listOfEmpty.shift();

  // We find chosen element and display it
  const newImageForm = $(".image-form").eq(first);
  newImageForm.removeClass("d-none");
}

function saveEvent(event) {
  event.preventDefault();
  $(".image-form").find("input").prop("disabled", false);
  $("#main-form").trigger("submit");
}

function deleteImage(event) {
  event.preventDefault();
  const image_id = $(this).attr('id').slice(14);
  $("#delete-form-" + image_id).trigger("submit");
}

$(function() {
  // We get number of image forms received from server.
  maxFormsetNumber = parseInt($('input[name="image_set-TOTAL_FORMS"]').val());

  // We get number of extra image forms (empty ones) received from server
  extraImagesNumber = parseInt($("#extra-images-number").val());

  // Extra images in formset should remain hidden, as they are empty.
  formsetCounter = maxFormsetNumber - extraImagesNumber;

  if(formsetCounter === 0)formsetCounter++;

  // We add position of available image forms to listOfEmpty.
  $(".image-form").slice(0, formsetCounter).removeClass("d-none");

  for (let i = formsetCounter; i < maxFormsetNumber; i++) {
    listOfEmpty.push(i);
  }

  $(".image-form label").empty();

  $("#new-image-form").on(
      "click",
      newImageClick
  );

  $("#save-defect").on(
      "click",
      saveEvent
  )

  $(".delete-photo-button").on(
      "click",
      deleteImage
  )
});