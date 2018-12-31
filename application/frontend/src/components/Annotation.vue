<template>
  <div v-if="showAnno">
    <!-- Text annotation button -->
    <b-button @click="modalShow = !modalShow" id="bubble" variant="dark" :style="bubbleStyle">
      <h5 class="mb-0">
        <strong>
          <font-awesome-icon icon="edit" fixed-width/>Annotate
        </strong>
      </h5>
    </b-button>

    <!-- Image annotation button -->
    <b-button
      @click="imageModalShow = !imageModalShow"
      id="bubbleImage"
      variant="dark"
      :style="imageBubbleStyle"
    >
      <h5 class="mb-0">
        <strong>
          <font-awesome-icon icon="edit" fixed-width/>Annotate
        </strong>
      </h5>
    </b-button>

    <!-- Text annotation modal -->
    <b-modal v-model="modalShow" title="Annotate" @ok="sendTextAnnotation" ok-title="Annotate">
      <p>
        <strong>Text to annotate:</strong>
        {{selectedText}}
      </p>
      <div class="ql-snow">
        <vue-editor
          class="unique"
          useCustomImageHandler
          @imageAdded="handleImageAdded"
          v-model="annotationText"
          placeholder="Write your annotation"
        ></vue-editor>
      </div>
    </b-modal>

    <!-- Image annotation modal -->
    <b-modal
      v-model="imageModalShow"
      title="Annotate"
      @ok="sendImageAnnotation"
      ok-title="Annotate"
    >
      <div class="ql-snow">
        <vue-editor
          class="unique"
          useCustomImageHandler
          @imageAdded="handleImageAdded"
          v-model="annotationText"
          placeholder="Write your annotation"
        ></vue-editor>
      </div>
    </b-modal>

    <!-- Text annotation popup -->
    <div
      :id="`textanno${rect.id}`"
      :key="rect.id"
      v-for="rect in annotationClientRects"
      :style="rect.style"
    >
      <b-popover :target="`textanno${rect.id}`" triggers="hover click" placement="auto">
        <template slot="title">
          <div class="d-flex justify-content-between align-items-center">
            <router-link
              class="mr-1"
              :to="`/profile/${getUserIdFromAnno(textAnnotations[rect.annoIndex])}`"
            >
              <strong>{{textAnnotations[rect.annoIndex].creator.name}}</strong>
            </router-link>
            <small
              class="text-muted"
              v-b-tooltip.hover.bottom="$moment(textAnnotations[rect.annoIndex].created).format('LLLL')"
            >{{textAnnotations[rect.annoIndex].created | moment("from") }}</small>
          </div>
        </template>
        <div>
          <!-- ql-snow and ql-editor is necessary for quill editor styling -->
          <div class="unique2 ql-snow" :style="{'max-height':'60vh','overflow-y':'auto'}">
            <div class="ql-editor" v-html="textAnnotations[rect.annoIndex].body.value"></div>
          </div>
        </div>
      </b-popover>
    </div>

    <!-- Image annotation popup -->
    <div :id="`imageanno${rect.id}`" :key="rect.id" v-for="rect in imageRects" :style="rect.style">
      <b-popover :target="`imageanno${rect.id}`" triggers="hover click" placement="auto">
        <template slot="title">
          <div class="d-flex justify-content-between align-items-center">
            <router-link
              class="mr-1"
              :to="`/profile/${getUserIdFromAnno(imageAnnotations[rect.annoIndex])}`"
            >
              <strong>{{imageAnnotations[rect.annoIndex].creator.name}}</strong>
            </router-link>
            <small
              class="text-muted"
              v-b-tooltip.hover.bottom="$moment(imageAnnotations[rect.annoIndex].created).format('LLLL')"
            >{{imageAnnotations[rect.annoIndex].created | moment("from") }}</small>
          </div>
        </template>
        <div>
          <!-- ql-snow and ql-editor is necessary for quill editor styling -->
          <div class="unique2 ql-snow" :style="{'max-height':'60vh','overflow-y':'auto'}">
            <div class="ql-editor" v-html="imageAnnotations[rect.annoIndex].body.value"></div>
          </div>
        </div>
      </b-popover>
    </div>
  </div>
</template>

<script>
import { VueEditor } from "vue2-editor";
import Croppr from "croppr";
import "croppr/dist/croppr.min.css";

export default {
  name: "Annotation",
  components: {
    VueEditor
  },
  data() {
    return {
      modalShow: false,
      imageModalShow: false,
      annotationText: "",
      textAnnotations: [],
      imageAnnotations: [],
      annotationClientRects: [],
      imageRects: [],
      bubbleStyle: {
        visibility: "hidden",
        position: "absolute",
        top: 0,
        left: 0,
        "z-index": "11"
      },
      imageBubbleStyle: {
        visibility: "hidden",
        position: "absolute",
        top: 0,
        left: 0,
        "z-index": "11"
      },
      selectedArea: {
        x: 0,
        y: 0,
        w: 0,
        h: 0
      },
      annoImageSource: "",
      selectedText: "",
      startSelectorXPath: "",
      startSelectorStartOffset: 0,
      startSelectorEndOffset: 0,
      endSelectorXPath: "",
      endSelectorStartOffset: 0,
      endSelectorEndOffset: 0,
      cropprInstance: {}
    };
  },
  computed: {
    showAnno: function() {
      return this.$root.$data.annoSetting == "show";
    }
  },
  created() {
    this.fetchTextAnnotation();
    this.fetchImageAnnotation();
  },
  watch: {
    $route(to, from) {
      this.modalShow = false;
      this.imageModalShow = false;
      this.bubbleStyle.visibility = "hidden";
      this.imageBubbleStyle.visibility = "hidden";
      this.textAnnotations = [];
      this.imageAnnotations = [];
      this.annotationClientRects = [];
      this.imageRects = [];
      this.fetchTextAnnotation();
      this.fetchImageAnnotation();
    }
  },
  methods: {
    mouseup(e) {
      const selectedText = this.getSelectedText();
      if (selectedText && !this.modalShow) {
        if (this.bubbleStyle.visibility != "visible") {
          this.renderBubble(e.pageX, e.pageY);
        }

        this.selectedText = selectedText;

        const startNode = window.getSelection().getRangeAt(0).startContainer;
        const endNode = window.getSelection().getRangeAt(0).endContainer;
        const startOffset = window.getSelection().getRangeAt(0).startOffset;
        const endOffset = window.getSelection().getRangeAt(0).endOffset;
        const startNodeLength = startNode.length; // highlight end

        this.startSelectorXPath = this.getXPath(startNode);
        this.endSelectorXPath = this.getXPath(endNode);
        if (startNode == endNode) {
          this.startSelectorStartOffset = startOffset;
          this.startSelectorEndOffset = endOffset;
          this.endSelectorStartOffset = startOffset;
          this.endSelectorEndOffset = endOffset;
        } else {
          this.startSelectorStartOffset = startOffset;
          this.startSelectorEndOffset = startNodeLength;
          this.endSelectorStartOffset = 0;
          this.endSelectorEndOffset = endOffset;
        }
      }
      const qlEditor = document.querySelector(".ql-container");
      if (
        e.target.nodeName == "IMG" &&
        ((qlEditor && !qlEditor.contains(e.target)) || !qlEditor)
      ) {
        e.target.classList.add("mycroppr");
        this.cropprInstance = new Croppr(".mycroppr", {
          startSize: [50, 50],
          onCropEnd: data => {
            this.selectedArea.x = data.x;
            this.selectedArea.y = data.y;
            this.selectedArea.w = data.width;
            this.selectedArea.h = data.height;
          },
          onInitialize: instance => {
            const data = instance.getValue();
            this.selectedArea.x = data.x;
            this.selectedArea.y = data.y;
            this.selectedArea.w = data.width;
            this.selectedArea.h = data.height;
          }
        });
        this.annoImageSource = document.querySelector(".croppr-image").src;
        this.renderImageBubble();
      }
    },
    renderImageBubble() {
      const cropprPos = document
        .querySelector(".croppr")
        .getBoundingClientRect();
      this.imageBubbleStyle.left = cropprPos.left + "px";
      this.imageBubbleStyle.top = cropprPos.bottom + 2 + "px";
      this.imageBubbleStyle.visibility = "visible";
    },
    renderBubble(mouseX, mouseY) {
      const offsetWidth = document.getElementById("bubble").offsetWidth;
      if (mouseX + offsetWidth > window.innerWidth - 20) {
        this.bubbleStyle.left = window.innerWidth - offsetWidth - 20 + "px";
      } else {
        this.bubbleStyle.left = mouseX + "px";
      }
      this.bubbleStyle.top = mouseY + "px";
      this.bubbleStyle.visibility = "visible";
    },
    getSelectedText() {
      let text = "";
      if (typeof window.getSelection != "undefined") {
        text = window.getSelection().toString();
      }
      return text;
    },
    getXPath(node) {
      if (node.nodeType == Node.ELEMENT_NODE && node.id != "") {
        return '//*[@id="' + node.id + '"]';
      }
      if (node === document.documentElement) {
        return "/" + this.getNodeName(node);
      }
      let siblingIndex = 0;
      const siblings = node.parentNode.childNodes;
      for (let i = 0; i < siblings.length; i++) {
        const sibling = siblings[i];
        if (sibling === node) {
          return (
            this.getXPath(node.parentNode) +
            "/" +
            this.getNodeName(node) +
            "[" +
            (siblingIndex + 1) +
            "]"
          );
        }
        if (
          sibling.nodeType === node.nodeType &&
          sibling.nodeName === node.nodeName
        ) {
          siblingIndex++;
        }
      }
    },
    getNodeName(node) {
      const nodeName = node.nodeName.toLowerCase();
      if (nodeName == "#text") {
        return "text()";
      } else if (nodeName == "#comment") {
        return "comment()";
      } else if (nodeName == "#cdata-section") {
        return "cdata-section()";
      } else {
        return nodeName;
      }
    },
    mousedown(e) {
      const bubble = document.getElementById("bubble");
      const bubbleImage = document.getElementById("bubbleImage");
      if (bubble.contains(e.target)) {
        // Clicked in box
      } else {
        // Clicked outside the box
        this.bubbleStyle.visibility = "hidden";
        this.bubbleStyle.top = "0px";
        this.bubbleStyle.left = "0px";
      }

      // when an image has area selection
      if (document.querySelector(".croppr") !== null) {
        // destroy croppr instance when clicked outside the image
        if (
          !e.target.classList.contains("croppr") &&
          !bubbleImage.contains(e.target)
        ) {
          this.imageBubbleStyle.visibility = "hidden";
          this.cropprInstance.destroy();
          document.querySelector(".mycroppr").classList.remove("mycroppr");
        }
      }
    },
    sendTextAnnotation() {
      this.$axios
        .post(`/annotation/textannotation/`, {
          type: "Annotation",
          body: {
            type: "TextualBody",
            language: "en",
            value: this.annotationText
          },
          target: {
            source: window.location.href,
            selector: {
              type: "RangeSelector",
              startSelector: {
                type: "XPathSelector",
                value: this.startSelectorXPath,
                refinedBy: {
                  type: "TextPositionSelector",
                  start: this.startSelectorStartOffset,
                  end: this.startSelectorEndOffset
                }
              },
              endSelector: {
                type: "XPathSelector",
                value: this.endSelectorXPath,
                refinedBy: {
                  type: "TextPositionSelector",
                  start: this.endSelectorStartOffset,
                  end: this.endSelectorEndOffset
                }
              }
            }
          }
        })
        .then(response => {
          this.textAnnotations.push(response.data);
          this.calculateAnnotationClientRects();
          this.annotationText = "";
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    sendImageAnnotation() {
      this.$axios
        .post(`/annotation/imageannotation/`, {
          type: "Annotation",
          body: {
            type: "TextualBody",
            language: "en",
            value: this.annotationText
          },
          target: {
            source: this.annoImageSource,
            scope: window.location.href,
            selector: {
              type: "FragmentSelector",
              conformsTo: "http://www.w3.org/TR/media-frags/",
              value: `xywh=${this.selectedArea.x},${this.selectedArea.y},${
                this.selectedArea.w
              },${this.selectedArea.h}`
            }
          }
        })
        .then(response => {
          this.imageAnnotations.push(response.data);
          this.calculateImgAnnoRects();
          this.annotationText = "";
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    fetchTextAnnotation() {
      this.$axios
        .get(
          `/annotation/textannotation/?target__source=${window.location.href}`
        )
        .then(response => {
          this.textAnnotations = response.data;
          this.calculateAnnotationClientRects();
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    fetchImageAnnotation() {
      this.$axios
        .get(
          `/annotation/imageannotation/?target__scope=${window.location.href}`
        )
        .then(response => {
          this.imageAnnotations = response.data;
          this.calculateImgAnnoRects();
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    },
    calculateAnnotationClientRects() {
      this.annotationClientRects = [];
      let count = 0;
      for (let i = 0; i < this.textAnnotations.length; i++) {
        const annotation = this.textAnnotations[i];

        const startNode = document.evaluate(
          annotation.target.selector.startSelector.value,
          document,
          null,
          XPathResult.FIRST_ORDERED_NODE_TYPE,
          null
        ).singleNodeValue;
        const endNode = document.evaluate(
          annotation.target.selector.endSelector.value,
          document,
          null,
          XPathResult.FIRST_ORDERED_NODE_TYPE,
          null
        ).singleNodeValue;

        let startOffset;
        let endOffset;
        if (startNode == endNode) {
          startOffset =
            annotation.target.selector.startSelector.refinedBy.start;
          endOffset = annotation.target.selector.startSelector.refinedBy.end;
        } else {
          startOffset =
            annotation.target.selector.startSelector.refinedBy.start;
          endOffset = annotation.target.selector.endSelector.refinedBy.end;
        }

        let range = document.createRange();
        range.setStart(startNode, startOffset);
        range.setEnd(endNode, endOffset);

        let clientRects = range.getClientRects();
        for (let j = 0; j < clientRects.length; j++) {
          let obj = {};
          let rect = clientRects[j];
          let style = {};
          style.width = rect.width + "px";
          style.height = rect.height + "px";
          style.top = rect.y + "px";
          style.left = rect.x + "px";
          style.position = "absolute";
          style.opacity = 0.3;
          style["z-index"] = 10;
          style.background = "#2196F3";
          //style["border-bottom"] = "0.3em solid #2196F3";
          obj.style = style;
          obj.annoIndex = i;
          obj.id = count;
          this.annotationClientRects.push(obj);
          count++;
        }
      }
    },
    getUserIdFromAnno(anno) {
      return anno.creator.id.split("/").slice(-2, -1)[0];
    },
    calculateImgAnnoRects() {
      this.imageRects = [];
      const images = document.getElementsByTagName("img");
      let count = 0;
      for (let i = 0; i < this.imageAnnotations.length; i++) {
        const imgAnno = this.imageAnnotations[i];
        const imgElement = this.findImgWithSrc(images, imgAnno.target.source);
        const imgScaling = imgElement.width / imgElement.naturalWidth;
        const imgRect = imgElement.getBoundingClientRect();
        const selectorValueStr = imgAnno.target.selector.value;
        let selectorValue = selectorValueStr.substring(
          selectorValueStr.indexOf("=") + 1
        );
        selectorValue = selectorValue
          .split(",")
          .map(Number)
          .map(x => x * imgScaling);
        let style = {
          left: imgRect.left + selectorValue[0] + "px",
          top: imgRect.top + selectorValue[1] + "px",
          width: selectorValue[2] + "px",
          height: selectorValue[3] + "px",
          position: "absolute",
          border: "4px solid rgba(33,150,243,.4)",
          //opacity: 0.3,
          "z-index": 10
          //background: "#2196F3"
        };
        this.imageRects.push({
          id: count,
          annoIndex: i,
          style: style
        });
        count++;
      }
    },
    findImgWithSrc(images, src) {
      for (let i = 0; i < images.length; i++) {
        if (images[i].src == src) {
          return images[i];
        }
      }
    },
    handleImageAdded(file, Editor, cursorLocation, resetUploader) {
      let formData = new FormData();
      formData.append("url", file);

      this.$axios({
        url: "/upload/image/",
        method: "POST",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
        .then(response => {
          let url = response.data.url;
          Editor.insertEmbed(cursorLocation, "image", url);
          resetUploader();
        })
        .catch(err => {
          // eslint-disable-next-line
          console.log(err);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>