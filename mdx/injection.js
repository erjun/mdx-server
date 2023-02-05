//inhections.js

var audio_type = {
  mp3: "audio/mpeg",
  mp4: "audio/mp4",
  wav: "audio/wav",
  spx: "audio/ogg",
  ogg: "audio/ogg",
};

function audio_content_type(ext) {
  return audio_type[ext] || "audio/mpeg";
}

function getDictTydpe() {
  if ($(".lm5ppbody").length) return "lm5";
  if ($("#v5A").length) return "v5a";
}

function lm5Init() {
  let has = false;
  const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });
  let pos = params.pos;
  let $dicts = $(".dictentry:not(.bussdict)");
  $dicts
    .find(".lm5pp_POS")
    .each((i, elem) => {
      if (has) return;
      if ($(elem).text().trim().indexOf(pos) > -1) {
        has = true;
        let $curDict = $(elem).parents(".dictentry");

        $curDict
          .find(".foldsign_fold")
          .each((i, elem) => {
            $(elem).click();
          });
        if ($dicts.index($curDict) > 0) {
          $(elem).parents(".dictentry")[0].scrollIntoView();
        }

      }
    });
  if (pos && !has) {
    alert(pos + "未找到");
  }
}

function v5aInit() {
  $("#vUi")[0].scrollIntoView();
}

$(document).ready(function () {
  $("body a").click(function () {
    var tag = $(this).attr("href");
    if (!tag) {
      return false;
    }
    if (tag.startsWith("sound://")) {
      $("#audiotag").attr("src", "/" + tag.substr("sound://".length));
      $("#audiotag").attr("type", audio_content_type(tag.slice(-3)));
      try {
        audioElement = document.getElementById("audiotag");
        audioElement.play();
        return false;
      } catch (err) { }
      return false;
    }
  });
  $("body .EXAMPLE a.speaker").each((i, e) => { $(e).attr('title', '') })

  let type = getDictTydpe();
  if (type == "lm5") {
    setTimeout(() => {
      lm5Init();
    }, 10);
  } else if (type == "v5a") {
    v5aInit();
  }
});

