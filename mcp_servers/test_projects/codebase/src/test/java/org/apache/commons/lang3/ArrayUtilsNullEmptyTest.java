package org.apache.commons.lang3;

import org.junit.Test;
import static org.junit.Assert.*;

public class ArrayUtilsNullEmptyTest {

    @Test
    public void testNullToEmptyObjectArrayReturnsSharedEmpty() {
        Object[] out = ArrayUtils.nullToEmpty((Object[]) null);
        assertNotNull(out);
        assertEquals(0, out.length);
        assertSame(ArrayUtils.EMPTY_OBJECT_ARRAY, out);
    }

    @Test
    public void testCloneNullReturnsNull() {
        Integer[] input = null;
        Integer[] out = ArrayUtils.clone(input);
        assertNull(out);
    }

    @Test
    public void testGetLengthNullAndNonArray() {
        assertEquals(0, ArrayUtils.getLength(null));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetLengthNonArrayThrows() {
        ArrayUtils.getLength("not an array");
    }
}
