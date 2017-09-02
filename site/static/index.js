var list, folder, image, rank_input, current_image_src;

$(function () {
    list = $("#csv").text().split(",");
    console.log(list);
    folder = $("#folder").text();

    image = $("#face");
    rank_input = $("#rank");

    make_random_face();
    rank_input.focus();

    $("#inputs").on("submit", function (e) {
        var value = rank_input.val();

        $.get("/save", {"filename": current_image_src, "rank": value});

        make_random_face();
        rank_input.val("").focus();

        e.preventDefault();
    });
});

function make_random_face() {
    var random_index = Math.floor(Math.random() * list.length);
    console.log(random_index);

    current_image_src = list[random_index];
    list.splice(random_index, 1);
    console.log(list.length);

    image_src = "./" + folder + "/" + current_image_src;
    image.attr("src", image_src)
}