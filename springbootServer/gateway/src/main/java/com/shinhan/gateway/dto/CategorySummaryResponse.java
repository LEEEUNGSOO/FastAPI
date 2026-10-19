package com.shinhan.gateway.dto;
// FastAPI CategorySummary 모델과 짝
public record CategorySummaryResponse(String category, Integer count, Long total) {}

/* ===== 전체 이해 =====
 * - 카테고리별 건수·합계 한 줄. List<CategorySummaryResponse> 로 받음
 * - public record 하나에 파일 하나. 세 record를 한 파일에 모으면 컴파일 에러
 */