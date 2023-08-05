def normalizeMetaHeaders(metadata):
    metadataHeaders = {}
    items = metadata.items()

    for kvp in items:
        key = kvp[0]
        value = kvp[1]
        lowerCaseKey = key.lower()
        if lowerCaseKey.startswith('x-imagine-meta-'):
            metadataHeaders[lowerCaseKey] = value
        else:
            newKey = "x-imagine-meta-{0}".format(lowerCaseKey)
            metadataHeaders[newKey] = value
    
    return metadataHeaders