package test.java.org.apache.commons.lang3;

import org.junit.Test;
import static org.junit.Assert.*;

public class ArrayUtilsSubarrayIndexOfTest {

    @Test
    public void testSubarrayBoundsAndContents() {
        Integer[] arr = new Integer[] {1,2,3,4,5};
        Integer[] sub = ArrayUtils.subarray(arr, -2, 10);
        assertArrayEquals(new Integer[] {1,2,3,4,5}, sub);

        Integer[] empty = ArrayUtils.subarray(arr, 3, 3);
        assertEquals(0, empty.length);
    }

    @Test
    public void testIndexOfAndLastIndexOfObjectArray() {
        String[] arr = new String[] {"a", null, "b", "a"};
        assertEquals(0, ArrayUtils.indexOf(arr, "a"));
        assertEquals(3, ArrayUtils.lastIndexOf(arr, "a"));
        assertEquals(1, ArrayUtils.indexOf(arr, null));
        assertEquals(ArrayUtils.INDEX_NOT_FOUND, ArrayUtils.indexOf(arr, "z"));
    }

    @Test
    public void testIndexOfPrimitives() {
        int[] iarr = new int[] {5,6,7,6};
        assertEquals(1, ArrayUtils.indexOf(iarr, 6));
        assertEquals(3, ArrayUtils.lastIndexOf(iarr, 6));
        assertEquals(ArrayUtils.INDEX_NOT_FOUND, ArrayUtils.indexOf(iarr, 9));
    }
}
