package com.shopwave.filter;

import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class IdempotencyFilter implements Filter {

    private static final String HEADER_NAME = "Idempotency-Key";

    private final Set<String> processedKeys = ConcurrentHashMap.newKeySet();

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String key = httpRequest.getHeader(HEADER_NAME);

        if (key != null && !key.isBlank()) {
            boolean isNewKey = processedKeys.add(key);

            if (!isNewKey) {
                httpResponse.setStatus(HttpServletResponse.SC_CONFLICT);
                httpResponse.getWriter().write("Duplicate request detected");
                return;
            }
        }

        chain.doFilter(request, response);
    }
}
