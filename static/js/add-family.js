$(document).ready(function () {
  var memberCounter = 1;

  addFamilyMember();

  function addFamilyMember() {
    var isValid = validateCurrentMember();
    if (!isValid) {
      console.log("Please fill in all compulsory fields before adding a new member.");
      return;
    }
    // Update the value of the hidden input field
    $("#memberCounter").val(memberCounter);
  }

  function validateCurrentMember() {
    // Check if all compulsory fields in the current family member are filled
    var currentMember = $(".family-member:last");
    var inputs = currentMember.find("input[required]");
    var isValid = true;

    inputs.each(function () {
      if ($(this).val() === "") {
        isValid = false;
        return false; // Break the loop if any field is empty
      }
    });

    return isValid;
  }

  // Event listener for "Add Family Member" button
  $("#add-member-btn").on("click", function () {
    addFamilyMember();
  });

  // Event listener for checkbox change
  $(".family-member").on("change", ".vaccine-status", function () {
    var vaccineReceivedInput = $(this)
      .closest(".row")
      .find(".vaccine-received-input");

    if ($(this).prop("checked")) {
      // Show the vaccine received input field
      vaccineReceivedInput.show();
    } else {
      // Hide the vaccine received input field
      vaccineReceivedInput.hide();
    }
  });
});
