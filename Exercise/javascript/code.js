/** The function is about the the quick sort algorithm */

/**
 * @function partitions
 * @param {array} array - given a array
 * @param {integer} p - the most left index
 * @param {integer} r - the most right index
 * @return {integer} i - the pivot elemnt index after sorting
 */
var partition = function(array, p, r) {
  // This code has been purposefully obfuscated,
  // as you will implement it yourself in next challenge
  var e = array,
    t = p,
    n = r;
  var r = function(e, t, n) {
    var r = e[t];
    e[t] = e[n];
    e[n] = r;
  };

  var i = t;

  for (var s = t; s < n; s++) {
    if (e[s] <= e[n]) {
      r(e, s, i);
      i++;
    }
  }
  r(e, n, i);
  return i;
};

/**
 * @function quickSort - use the partitions to sort the array
 * @param {array} array - given a array
 * @param {integer} p - the most left index
 * @param {integer} r - the most right index
 */

var quickSort = function(array, p, r) {
  if (p < r) {
    var i = partition(array, p, r);
    quickSort(array, p, i - 1);
    quickSort(array, i + 1, r);
  }
};