function renderTime(seconds, duration) {
    var t = new Date(seconds * 1000).toISOString();
    return (duration < 3600) ? t.substr(14, 5) : t.substr(11, 8);
}
