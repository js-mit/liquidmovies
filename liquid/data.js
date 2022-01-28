// import * as data from "./data.json";
// const { name } = data;
// console.log(name); // output 'testing'

var arrayOfObjects = [
  {
    Timestamp: 0,
    Label: {
      Name: "Animal",
      Confidence: 99.92265319824219,
      Instances: [],
      Parents: [],
    },
    FrameURL:
      "https://liquid-s3-dev-0.s3.amazonaws.com/users/1/videos/4/liquids/4/frames/0.jpg",
  },
  {
    Timestamp: 0,
    Label: {
      Name: "Mammal",
      Confidence: 99.92265319824219,
      Instances: [],
      Parents: [{ Name: "Animal" }],
    },
    FrameURL:
      "https://liquid-s3-dev-0.s3.amazonaws.com/users/1/videos/4/liquids/4/frames/0.jpg",
  },
  {
    Timestamp: 0,
    Label: {
      Name: "Rock",
      Confidence: 63.410709381103516,
      Instances: [],
      Parents: [],
    },
    FrameURL:
      "https://liquid-s3-dev-0.s3.amazonaws.com/users/1/videos/4/liquids/4/frames/0.jpg",
  },
  {
    Timestamp: 0,
    Label: {
      Name: "Tiger",
      Confidence: 99.92265319824219,
      Instances: [
        {
          BoundingBox: {
            Width: 0.16532544791698456,
            Height: 0.440255731344223,
            Left: 0.4529847502708435,
            Top: 0.44716984033584595,
          },
          Confidence: 99.91724395751953,
        },
        {
          BoundingBox: {
            Width: 0.15300707519054413,
            Height: 0.37313956022262573,
            Left: 0.6988927125930786,
            Top: 0.5922809839248657,
          },
          Confidence: 99.85367584228516,
        },
        {
          BoundingBox: {
            Width: 0.16612955927848816,
            Height: 0.43701595067977905,
            Left: 0.28356412053108215,
            Top: 0.4985453188419342,
          },
          Confidence: 99.50923156738281,
        },
        {
          BoundingBox: {
            Width: 0.24696139991283417,
            Height: 0.4496486186981201,
            Left: 0.33171606063842773,
            Top: 0.46710899472236633,
          },
          Confidence: 64.31562805175781,
        },
      ],
      Parents: [{ Name: "Wildlife" }, { Name: "Mammal" }, { Name: "Animal" }],
    },
    FrameURL:
      "https://liquid-s3-dev-0.s3.amazonaws.com/users/1/videos/4/liquids/4/frames/0.jpg",
  },
];

console.log(arrayOfObjects[0]);
console.log(arrayOfObjects[0]["Label"]["Name"]);

// load json using require (error)
// const arr = require("./data.json");
// console.log(arr);

// load json using fetch (error)
function getData() {
  fetch("./data.json")
    .then((response) => {
      return response.json();
    })
    .then((data) => console.log(data));
}
getData();

// find occurence of each key
function findOcc(arr, key) {
  let arr2 = [];

  arr.forEach((object) => {
    // Checking if there is any object in arr2
    // which contains the key value
    if (
      arr2.some((obj) => {
        return obj["Label"] === object["Label"][key];
      })
    ) {
      // If yes then increase the occurrence by 1
      arr2.forEach((obj) => {
        if (obj[key] === object["Label"][key]) {
          obj["occurrence"]++;
        }
      });
    } else {
      // If not Then create a new object initialize
      // it with the present iteration key's value and
      // set the occurrence to 1
      let newObject = {};
      newObject[key] = object["Label"][key];
      newObject["occurrence"] = 1;
      arr2.push(newObject);
    }
  });

  return arr2;
}

const key = "Name";
console.log("unsorted:", findOcc(arrayOfObjects, key));

// // sort the array
const unsortarr = findOcc(arrayOfObjects, key);
const sortarr = unsortarr.sort(function (a, b) {
  console.log(a.occurrence, b.occurrence);
  return b.occurrence - a.occurrence;
});
console.log("sorted:", sortarr);

// sample test

// let arr = [
//   {
//     employeeName: "Shyam",
//     employeeId: 24,
//   },
//   {
//     employeeName: "Ram",
//     employeeId: 23,
//   },

//   {
//     employeeName: "Ram",
//     employeeId: 21,
//   },
//   {
//     employeeName: "Ram",
//     employeeId: 25,
//   },
//   {
//     employeeName: "Kisan",
//     employeeId: 22,
//   },
//   {
//     employeeName: "Shyam",
//     employeeId: 20,
//   },
// ];

// function findOcc(arr, key) {
//   let arr2 = [];

//   arr.forEach((object) => {
//     console.log(object);
//     console.log(object[key]);

//     if (
//       arr2.some((obj) => {
//         return obj[key] === object[key];
//       })
//     ) {
//       arr2.forEach((obj) => {
//         if (obj[key] === object[key]) {
//           obj["occurrence"]++;
//         }
//       });
//     } else {
//       let newObject = {};
//       newObject[key] = object[key];
//       newObject["occurrence"] = 1;
//       arr2.push(newObject);
//     }
//   });

//   return arr2;
// }

// const key = "employeeName";
// console.log("unsorted", findOcc(arr, key));

// const unsortarr = findOcc(arr, key);

// // sort the array
// const sortarr = unsortarr.sort(function (a, b) {
//   console.log(a.occurrence, b.occurrence);
//   return b.occurrence - a.occurrence;
// });
// console.log(sortarr);
