package org.apache.commons.lang3;

import org.junit.Test;
import static org.junit.Assert.*;

import java.util.AbstractMap;
import java.util.Map;

public class ArrayUtilsToMapTest {

    @Test
    public void testToMapWithArrayPairs() {
        Object[] pairs = new Object[] { new Object[] {"k1","v1"}, new Object[] {"k2","v2"} };
        Map<Object,Object> m = ArrayUtils.toMap(pairs);
        assertEquals(2, m.size());
        assertEquals("v1", m.get("k1"));
    }

    @Test
    public void testToMapWithMapEntry() {
        Map.Entry<String,String> e = new AbstractMap.SimpleEntry<>("x","y");
        Object[] input = new Object[] { e };
        Map<Object,Object> m = ArrayUtils.toMap(input);
        assertEquals("y", m.get("x"));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testToMapWithMalformedElementThrows() {
        Object[] bad = new Object[] { "not a pair" };
        ArrayUtils.toMap(bad);
    }
}
